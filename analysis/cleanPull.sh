node src/pull.js > results/data.json
echo "Cleaning data and placing in results/data.json."
python3 src/cleanPull.py
python3 src/pull.py
