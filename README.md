# Feel-Me
An emotion detection based music visualiser using Python and Arduino

### Project Demonstration
Link: <a href="https://youtu.be/EfjZjk3YLvU">See here</a>

### Programming Languages Used
<ol>
  <li>Python</li>
  <li>Arduino (C++)</li>
</ol>

### Python Libraries Used
<ol>
  <li>deepface Library from Facebook</li>
  <li>haarcascade_frontalface_default.xml</li>
  <li>OpenCV</li>
  <li>spotipy</li>
  <li>dotenv</li>
  <li>csv</li>
  <li>random</li>
</ol>

### API Support
<ol>
  <li>Spotify Web API</li>
</ol>


### References
Audio Features for Music Emotion Recognition: A Survey by Renato Panda; Ricardo Malheiro; Rui Pedro Paiva<br>
Find the article <a href="https://doi.ieeecomputersociety.org/10.1109/TAFFC.2020.3032373">here</a>.

<br>

### Additional Required Files
Create a .env file containing below information after getting a developer spotify account of yours.<br>
<b>NOTE: </b>The playback function only work for premium users. <br><br>

CLIENT_ID = YOUR_CLINET_ID<br>
CLIENT_SECRET = YOUR_CLINET_SECRET<br>
REDIRECT_URL =  A_REDIRECT_URL<br>
SCOPE = user-read-playback-state, user-modify-playback-state<br><br>

<b>NOTE: </b> Do not change the SCOPE parameters.
