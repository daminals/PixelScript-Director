# update entire project

cd script-gen 
./zip.sh
cd ..

echo "Updated script-gen"

cd process-audio
./zip.sh &
cd ..

echo "Updated process-audio"

cd process-video
./zip.sh & 
cd ..

echo "Updated process-video"

cd combine-audio
./zip.sh &
cd ..

echo "Updated combine-audio"

cd combine-video
./upload.sh &
cd ..

echo "Updated combine-video"

echo "Done"