# voice_recognition

To use the model, follow the steps below:
1. Access the vneural.py, change the keyword at line 146, where collection of keyword label occurs
  Keyword given in example is 'nhu'
2. Create folder 'train/' where contains keyword samples and non-keyword samples
3. Run vneural.py and see how it works


Update 23-5-2019: Forget the steps above ...

# using my NEW voice recognition design:
1. Have access to standardize.py for formatting .wav files to the standard form (i.e. to 44.1kHz wave and mix with silence recordings)
Mean that you have to get at list 3 folder with: sliences, A_KEY_WORD, NON_KEY_WORDS folder, each contains samples representing the label
2. Start training with train.py, just run train.py but mention the 'dictionairy' (folder:label) at line 98 which you have to configure them correctly. Once training completed, with automatical a file name 'model.keras' is created
3. Use the 'model.keras' to test. Example testing is prepared in 'usage.py'. It both uses the trained neural network and Google speech recognition. Enjoy the experiments

Contact me at fb.me/vinhphuc.tadang if any issue exists or contribute to the project (not really a project :) )



