// index.js

var folder_name;
// function checkVideoAvailability(videoURL) {
//     var xhr = new XMLHttpRequest();
//     xhr.open('HEAD', videoURL, true);
//     xhr.onreadystatechange = function() {
//         if (xhr.readyState === 4) {
//             if (xhr.status === 200) {  // Video is available
//                 document.getElementById("generatedVideo").src = videoURL;
//                 document.getElementById("videoContainer").style.display = "flex";
//                 document.getElementById("wait-video").style.display = "none"; // Show the video container
//                 console.log("Video is now available.");
//             } else {
//                 console.log("Video not available yet, retrying...");
//                 setTimeout(function() { checkVideoAvailability(videoURL); }, 30000); // Retry after 3 seconds
//             }
//         }
//     };
//     xhr.send();
// }

function checkVideoAvailability(videoURL) {
  fetch(videoURL, { method: 'HEAD' })
      .then(response => {
          if (response.ok) {
              document.getElementById("generatedVideo").src = videoURL;
              document.getElementById("videoContainer").style.display = "flex";
              document.getElementById("wait-video").style.display = "none"; // Show the video container
              console.log("Video is now available.");
          } else {
              console.log("Video not available yet, retrying...");
              setTimeout(function () { checkVideoAvailability(videoURL); }, 15000); // Retry after 15 seconds
          }
      })
      .catch(error => {
          console.error("Error checking video availability:", error);
      });
}

// function submitEditedScript() {
//         var xhr = new XMLHttpRequest();
//         var editedScript = document.getElementById("editedScript").value;
//         var topic = encodeURIComponent(document.getElementById("topic").value);
//         var url = "https://00z0vb71ui.execute-api.us-east-1.amazonaws.com/default/generate_video";  // Replace with your second API Gateway endpoint

//         xhr.open("POST", url, true);
//         xhr.setRequestHeader("Content-Type", "application/json");

//         xhr.onreadystatechange = function () {
//             if (xhr.readyState === 4 && xhr.status === 200) {
//                 // Handle response here, e.g., show a success message
//                 console.log("Edited script submitted successfully.");
//                 document.getElementById("wait-video").style.display = "flex";
//                 var json = JSON.parse(xhr.responseText);
//                 console.log(json)
//                 if(json.folder_name){
//                     var videoURL = "https://gpt3-video-scripts.s3.amazonaws.com/"+json.folder_name+"/output.mp4"
//                     checkVideoAvailability(videoURL);
//                 }
//                 //document.getElementById("editedScript").innerHTML = json.folder_name
//             }
//         };

//         var data = JSON.stringify({
//             "script": editedScript,
//             "directory": folder_name,
//             "topic": topic
//         });
//         xhr.send(data);
//     }

function submitEditedScript() {
  const editedScript = document.getElementById("editedScript").value;
  const topic = encodeURIComponent(document.getElementById("topic").value);
  const url = "https://00z0vb71ui.execute-api.us-east-1.amazonaws.com/default/generate_video";  // Replace with your second API Gateway endpoint
  // Check if captions are enabled
  const enableCaptions = document.getElementById("enableCaptions").checked;
  console.log("Captions enabled:", enableCaptions)

  fetch(url, {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({
          "script": editedScript,
          "directory": folder_name,
          "topic": topic,
          "caption_enabled": enableCaptions
      }),
  })
      .then(response => {
          if (response.ok) {
              console.log("Edited script submitted successfully.");
              document.getElementById("wait-video").style.display = "flex";
              return response.json();
          } else {
              throw new Error("Error submitting edited script");
          }
      })
      .then(json => {
          console.log(json);
          if (json.folder_name) {
              const videoURL = `https://gpt3-video-scripts.s3.amazonaws.com/${json.folder_name}/output.mp4`;
              checkVideoAvailability(videoURL);
          }
      })
      .catch(error => {
          console.error("Error submitting edited script:", error);
      });
}

// function submitForm() {
//     var xhr = new XMLHttpRequest();
//     var director = encodeURIComponent(document.getElementById("director").value);
//     var topic = encodeURIComponent(document.getElementById("topic").value);
//     //var url = "https://ebub88mu4l.execute-api.us-east-1.amazonaws.com/Dev/Dalle?director=" + director + "&topic=" + topic;
//     var url = "https://00z0vb71ui.execute-api.us-east-1.amazonaws.com/default/scriptGen?director=" + director + "&topic=" + topic;
//     xhr.open("GET", url, true);

//     xhr.onreadystatechange = function () {
//         if (xhr.readyState === 4 && xhr.status === 200) {
//             var json = JSON.parse(xhr.responseText);
//             console.log(json);
//             // Display the generated script
//             folder_name = json.folder_name;
//             document.getElementById("editedScript").value = json.script;
//         }
//     };
//     xhr.send();
// }

function submitForm() {
  const director = encodeURIComponent(document.getElementById("director").value);
  const topic = encodeURIComponent(document.getElementById("topic").value);
  const url = `https://00z0vb71ui.execute-api.us-east-1.amazonaws.com/default/scriptGen?director=${director}&topic=${topic}`;

  fetch(url)
      .then(response => {
          if (response.ok) {
              return response.json();
          } else {
              throw new Error("Error submitting form");
          }
      })
      .then(json => {
          console.log(json);
          folder_name = json.folder_name;
          document.getElementById("editedScript").value = json.script;
      })
      .catch(error => {
          console.error("Error submitting form:", error);
      });
}

function darkmode() {
    var darkModeButton = document.getElementById('darkModeToggle');
    document.body.classList.toggle('dark-mode');

    // Change button color based on mode
    if (document.body.classList.contains('dark-mode')) {
        darkModeButton.style.backgroundColor = 'white';
        darkModeButton.style.color = 'black';
        darkModeButton.innerText = 'Lightmode';
    } else {
        darkModeButton.style.backgroundColor = 'black';
        darkModeButton.style.color = 'white';
        darkModeButton.innerText = 'Darkmode';
    }
}
function getRandomDirectorAndTopic() {
// TMDb endpoint for popular movies
    const moviesUrl = 'https://api.themoviedb.org/3/movie/popular?api_key=88d86996c88a6b47c495a29746c4b11e';

    // Fetch popular movies
    fetch(moviesUrl)
        .then(response => response.json())
        .then(data => {
            // Select a random movie from the list
            const randomMovie = data.results[Math.floor(Math.random() * data.results.length)];
            // Fetch credits for the selected movie
            fetchMovieCredits(randomMovie.id);
        })
        .catch(error => {
            console.log('Error fetching popular movies:', error);
        });

    // TMDb endpoint for movie genres
    const genresUrl = 'https://api.themoviedb.org/3/genre/movie/list?api_key=88d86996c88a6b47c495a29746c4b11e';

    // Fetch movie genres
    fetch(genresUrl)
        .then(response => response.json())
        .then(data => {
            const randomGenre = data.genres[Math.floor(Math.random() * data.genres.length)];
            document.getElementById("topic").value = randomGenre.name; // Using genre name as topic
        })
        .catch(error => {
            console.log('Error fetching genres:', error);
        });
}

function fetchMovieCredits(movieId) {
    const creditsUrl = `https://api.themoviedb.org/3/movie/${movieId}/credits?api_key=88d86996c88a6b47c495a29746c4b11e`;

    fetch(creditsUrl)
        .then(response => response.json())
        .then(data => {
            const director = data.crew.find(person => person.job === 'Director');
            if (director) {
                document.getElementById("director").value = director.name;
            }
        })
        .catch(error => console.error('Error fetching movie credits:', error));
}
const directors = [
    "Jordan Peele", "Jordan Peele", 
    "Quentin Tarantino", "Quentin Tarantino", 
    "Taika Waititi", "Taika Waititi", 
    "Steven Spielberg", 
    "Michael Bay", 
    "Steven Spielberg", 
    "Tim Burton", 
    "Wes Anderson", 
    "James Cameron"
];

const topics = [
    "the last slice of pizza everyone is too full to finish", "the last slice of pizza everyone is too full to finish", 
    "emotional love story between two meatballs", "emotional love story between two meatballs",
    "plucky little piece of rust code, eager to embed himself in the linux kernel", "plucky little piece of rust code, eager to embed himself in the linux kernel", 
    "Spaghetti Western about Cats", 
    "alien plot to overthrow the CEO of JP Morgan Chase, Jamie Dimon", 
    "ant crusaders on a mission to capture the holy land", 
    "captivating tale about pirates on Mars", 
    "traveling circus who performs on trains through the alps", 
    "a dog's expedition to a fridge storing delicious meat"
];
function getDirectorAndTopic() {
    const randomIndex = Math.floor(Math.random() * directors.length);
    document.getElementById("director").value = directors[randomIndex];
    document.getElementById("topic").value = topics[randomIndex];
}
