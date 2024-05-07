echo $(realpath $(pwd))
echo $(ls)
curl --output enit.zip https://object.pouta.csc.fi/OPUS-MT-models/en-it/opus-2019-12-04.zip
curl --output iten.zip https://object.pouta.csc.fi/OPUS-MT-models/it-en/opus-2019-12-18.zip

for file in *.zip; do
  unzip $file -d $(basename $file .zip);
done
