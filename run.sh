source ~/.bashrc

echo "Running yolox"
cd /home/rayb/Documents/yolox/
rm export/*
source venv/bin/activate
export PYTHONPATH="{PYTHONPATH}:/home/rayb/Documents/yolox/" && python tools/demo.py video -n yolox-x -c yolox_x.pth --path ../choreolyzer/in.mp4 --conf 0.75 --nms 0.45 --tsize 640 --save_result --device gpu
deactivate

echo "Moving files over"
rm ../motrv2/data/Dataset/mot/DanceTrack/test/blackpink/img1/*
rm ../motrv2/data/Dataset/mot/deb_db_motrv2.json
mv export/*.jpg ../motrv2/data/Dataset/mot/DanceTrack/test/blackpink/img1/
mv export/data.json ../motrv2/data/Dataset/mot/det_db_motrv2.json

echo "Running motrv2"
cd /home/rayb/Documents/motrv2/
conda activate motrv2
./tools/simple_inference.sh ./motrv2_dancetrack.pth

echo "Running visualizer"
cd tracker
python vis.py
conda deactivate

echo "Moving bp.txt, out.avi"
rm ../../choreolyzer/out.avi
rm ../../choreolyzer/blackpink.txt
mv out.avi ../../choreolyzer/out.avi
mv blackpink.txt ../../choreolyzer/out.txt

cd ../../choreolyzer
