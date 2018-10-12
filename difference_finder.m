#{
  difference_finder.m
 
Notes:
  * I have no idea what makes something a good or bad threshold. I just put
  random numbers in that looked good so that needs to be determined. It may
  be that different difficulties need different values? Who knows
  
  * This might not take inaudible vaules into account, but I dunno if they are
  in this file since it was converted from MP3 (lossy)
#} 

# As the song gets more intense (higher frequency), we want to generate more
# buttons to press

#{
 Open a file and return the metadata within it. Older Octave documentation
 doesn't seem to have what's returned, but version 4.4.1 (which this was written
 in) does have that information
 
 Link: https://octave.org/doc/v4.4.1/Audio-File-Utilities.html
#}

songInfo = audioinfo('song.wav')

#{
 audioread always returns audio data (y) as a matrix with the following format
  Audio Data Format (Clean up!)
    Rows: Audio Frames
    Columns: Channels
#}

[rawAudioData, sampRate] = audioread('song.wav');

#{
  *** WARNING ***
  This implementation relies heavily on the matrix structure that Octave uses to
  return the audio data
  *** WARNING ***
#}

rowCount = rows(rawAudioData)
frameCount = rowCount / 60;

# CHECK THIS SO THAT YOU ALWAYS GET A NICE CLEAN CUT
partition = (rowCount)/(2 * 735);
display(partition);
#{
This is where we actually check for differences in the audio data. 

  * This algorithm is very dumb in that it has no considerations for anything
    other than whether two basic sums are 'different enough' from each other
    
  1) Do this until we get to the end of the file...

  2) Take two samples
  
    samp1 = [frame_x0, frame_x1]
    samp2 = [frame_x2, frame_x3]
    
    where frame_x2 is just frame_x1 + 1. Currently each sample represents 1/60th
    of a second

  3) Take the sum of all the elements in each sample
  
    sum1 = sum(samp1)
    sum2 = sum(samp2)

  4) Compare the absolutle value of the difference between the sums against
  some (currently arbitrary) threshold. If the difference is greater than the
  threshold, we say that an 'event' has been 'triggered' somewhere between these
  two intervals and add the 'middle' (frame_x1) to a list containing all of the
  triggers
  
    if (|delta sums| > threshold)
      add frame_x1 to triggerList

  5) Move the position pointer to (frame_x3 + 1)
  
  *** WARNING ***
  THERE IS CURRENTLY NO REAL BOUNDS CHECKING
  *** WARNING ***

#}

# This points to a frame... it's used to not play more of the song than
# exists... ...
framePointer = 0;

# Initialize an empty list to store our triggers ... in case it's not obvious
triggers = [];

#diffThreshold = 30; # This might be determined via code later on

file = fopen("output.txt", "w");

while framePointer < partition
  
  #{
  *** CHANGE 735 TO THE APPROPRIATE VARIABLE ***
  #}
  
  f_0 = (735 * 2 * framePointer) + 1;
  f_1 = f_0 + 735;
  
  f_2 = (735 * (2 * framePointer + 1)) + 2;
  f_3 = (735 * 2 * (framePointer + 1));

  sampSum1 = sum(rawAudioData(f_0:1:f_1));
  sampSum2 = sum(rawAudioData(f_2:1:f_3));
  
  diff = abs(sampSum2 - sampSum1);
  
  highT = 70;
  medT  = 65;
  lowT  = 60;
  minT  = 55;
  
  up    = 0;
  down  = 0;
  left  = 0;
  right = 0;
    
  objCount = rows(triggers) + 1;
  
  # High
  if highT <= diff
      up    = 1;
      down  = 0;
      left  = 0;
      right = 0;
      triggers = vertcat(triggers, f_1);
  endif
  
  # Medium
  if (medT <= diff) && (diff < highT)
      up    = 0;
      down  = 1;
      left  = 0;
      right = 0;
      triggers = vertcat(triggers, f_1);
      #oString = "{'Up' : %i, 'Down' : %i, 'Left' : %i, 'Right' : %i} \n", up, down, left, right;
      #display(oString);
      #printf("{'Up' : %i, 'Down' : %i, 'Left' : %i, 'Right' : %i} \n", up, down, left, right);
  endif
  
  # Low
  if (lowT <= diff) && (diff < medT)
      up    = 0;
      down  = 0;
      left  = 1;
      right = 0;
      triggers = vertcat(triggers, f_1);
  endif
  
  # Min
  if (minT <= diff) && (diff < lowT)
    up    = 0;
    down  = 0;
    left  = 0;
    right = 1;
    triggers = vertcat(triggers, f_1);
  endif
  
  if ((up == 1) || (down == 1)) || ((left == 1) || (right == 1))
    #oStr1 = strjoin({'Note #', int2str(objCount)});
    #oStr2 = strjoin({' - Activation Frame: ', int2str(triggers(i))});
    #oStr3 = strjoin({oStr1, oStr2});
    fprintf(file, "Note # %i - Activation Frame: %i \n", rows(triggers), framePointer);
    #fdisp(file, oStr3);#, fdisp(file, '1');# - TIME INITIATED: %f [sec]\n', noteNum, timeInitiated);
    #oString = "{'Up' : %i, 'Down' : %i, 'Left' : %i, 'Right' : %i} \n", up, down, left, right;
    #printf("{'Up' : %i, 'Down' : %i, 'Left' : %i, 'Right' : %i} \n", up, down, left, right);
      #display(oString);
      #oString = "{'Up' : %i, 'Down' : %i, 'Left' : %i, 'Right' : %i} \n", up, down, left, right);
      #printf(file, oString);
      fprintf(file, "{'Up' : %i, 'Down' : %i, 'Left' : %i, 'Right' : %i} \n", up, down, left, right);
  endif
  
  framePointer = framePointer + 1;
endwhile

fclose(file);

#plot(triggers);

#{
For testing purposes only, take the list of triggers from above and play them
back. We have to add (a large) number of frames on either side of our trigger
in order to hear anything

The extra frames are necessarily large because even just 1/60th of a second
contains 735 frames...
#}


#This only plays the audio so we can ignore it for now
#{
i = 1;
while i < rows(triggers)
  pA = triggers(i) - (7*3012);
  pB = triggers(i) + (7*3012);
  [songInterval, fs] = audioread('song.wav', [pA, pB]);
  player = audioplayer (songInterval, 44100, 8);
  play (player);
  i = i + 1;
endwhile
#}

# Output the 'notes' to our beatmap file
#printf("Note: ['Wait' : %f, 'Up': False]", timeUntilNextNote);

#{

i = 1;
while i <= rows(triggers)
  oStr1 = strjoin({'Note #', int2str(i)});
  oStr2 = strjoin({' - Activation Frame: ', int2str(triggers(i))});
  oStr3 = strjoin({oStr1, oStr2});
  fdisp(file, oStr3);#, fdisp(file, '1');# - TIME INITIATED: %f [sec]\n', noteNum, timeInitiated);
  i = i + 1;
endwhile
#}