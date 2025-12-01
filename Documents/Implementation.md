**General Structure of the Program**

My project aims to predict the player's next move using patterns from previous rounds. This is done by implementing Markov chain modelling.The program is organized as follows:

**RPS_AI**

This was the original building block.This was a single model Markov chain predictor.Each instance stored transitions based on a specific memory length such as 1 previous move.It would update transition frequencies,learn from previous rounds and predict the most likely next move.

**Multi_RPS_AI**

This is what is currently being used for prediction of moves.This is a multi model manager that creates multiple RPS_AI models,each with different memory lengths.The idea behind it was that it evlauates all models,tracks their individual performance and the best perfoming model is picked to predict the next move. This allows the system to adapt to different player behaviours.

**move_storage.py**

This handles reading and writing of move history to a JSON file.It ensures that the games are retained,allowing the AI to retain its learning.


**Tests**

Tests are all covered in the testing document.Unit tests were used along with edge case tests and integration tests. All these were meant to ensure functional correctness,learning behaviou and model selection validity. All in all,the program follows a clean modular design.Prediction logic,data storage and tests are all sepearted  making the code easy to maintain and modify if needed in the future.


**Achieved Time and Space Complexities**

**Updating transitions**:For each new move,accessing and updating dictionary entries is O(1) time on average.

**Prediction**:Since the prediction checks a small dictionary of transitions,access by key is O(1) and selecting the most frequeny transition is O(1) also as we have at most 3 choices(r,p or s).

**Multi model evaluation**:For n amount of models(I used 5),to update all models and their scores and to select the best model is O(n) time but since n is quite small,in practice this is effectively also O(1) time.

**File I/O for move_storage**:Read and write for a JSON depends on the size of stored history n.Reading and writing is O(n).This is the only part that grows with the size of the move history.

Overall **space complexity** is O(n).Each RPS_AI model stores transitions for its memory length.This memory will grow with the number of unique sequences observed during play.So in the worst case which could be a long game with random play.JSON history will also grow O(n).


**Performance and Big-O comparision**

Since all computations are constant time per roumd,the performance is dominated by the history size and the number of models.Thus in realistic use,the system will perform effectively even over hundreds of rounds.I/O operations are the slowest part in this project,but still fast enough for the project overall.


**Possible shortcomings and Suggestions for improvement**

**JSON file**:Storing every move in a JSON file will lead to it becoming quite large over time.So an improvement could be switching to SQLite for scalable persistence.

**Fixed number of models**:Currently the memory lengths are capped at 5.Improvements could be automatically increase or decrease the memory lengths depending of the player behaviour.


**Use of Large Language Models**

I used ChatGPT 5 and 5.1 quite a bit to help plan my project initially and help clarify concepts such as multi Markov chains.It also suggested adding an integration test file which I had not thought of.However,all the code is a 100 percent mine.The only code I used with ChatGPT's help was when I kept facing a bug for unittests due to my test files and ai_code file being in different folders.This meant that importing ai_code was not working in the test files,and hence I had to get help.Everything else is mine,documents are written solely by me as well.


**Sources Used:**

https://arxiv.org/pdf/2003.06769
This was the paper I used as reference when I switched to a multi model system.

https://www.geeksforgeeks.org/machine-learning/markov-chain/
This was used initially to learn about Markov chains.

https://docs.python.org/3/library/unittest.html
This was used to help me understand unittests as I had never used them before.

https://algolabra-hy.github.io/topics-en#machine-learning
The ideas page wasnt really a huge source,maybe only intitally for planning of the project.
