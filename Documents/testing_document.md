This project contains two core AI components:
RPS_AI — a single-model Markov chain–based Rock Paper Scissors predictor. Since this component is no longer utilized, I have not talked about its tests below.
Multi_RPS_AI — a multi-model system that evaluates several RPS_AI models with different memory lengths and selects the best-performing one.This is the method I currentl use to predict the next move.

My unit tests were designed to verify the correctness of these components in a reproducible manner. The tests focus on transition storage, prediction accuracy, model selection, and functional correctness.

**a,b,c,d,e is from tests_multi_ai.py**

**Testing the Multi-Model System (Multi_RPS_AI)**

**a. Testing Model Creation (test_models_created)**
Goal: Ensure the correct number of RPS_AI models are created with different memory lengths.

Method used:
Instantiate Multi_RPS_AI(max_m=5)
Verify that exactly 5 RPS_AI models exist
Validate that each is an instance of RPS_AI

Why:
The multi-model system relies on a range of submodels.

**b. Testing Update Across All Models (test_update_all_updates_models)**
Goal: Verify that player moves update every internal RPS model.

Method used:
Call update_all('p')
Check that each model’s prev_moves list was updated to ['p']

Why:
All submodels must learn simultaneously for fair performance comparison and selection of model per move.

**c. Testing Score Updating (test_update_model_scores)**
Goal: Ensure that update_scores() appends correct values of +1,-1 or 0 to all models,and ensures that the
list represents the most recent game outcomes only.

Method used:
Call ai.update_scores([+1,-1]),and check that all models have the score of +1,-1 exactly

Why:
Correct scoring is required for determining the best-performing model.

**d. Testing Best Model Selection (test_best_ai_selects_highest_score)**
Goal: Verify that the system picks the correct model based on recent scores.

Method used:
Give one model a strong score sequence (e.g., [+1, +1, +1, +1, +1])
Assert that best_ai() returns this model

Why:
Ensures the AI switches strategies correctly based on performance.

**e. Testing Final Move Selection (test_get_move_uses_best_model)**
Goal: Confirm that the multi-model system produces the correct AI move from the best-performing model.

Method used:
Force one model (index 0) to have the highest score
Mock its prediction to always return 'r'
Assert that get_move() returns the counter 'p'

Why:
This validates the complete flow i.e prediciton to pick a model to choose the final move.

**f and g are both from test_edge_cases.py**

**f. Testing Prediction with Insufficient Previous Moves (test_empty_prev_moves)**
Goal:
Verify that the AI behaves correctly when there are fewer previous moves than the memory length requires.

Method used:
Create an RPS_AI model with memory_length=3, but do not provide enough moves to form a valid key.
Call prediction() and ensure the returned move is one of r,p or s.

Why:
If the AI does not have enough history to form a sequence key, it should fall back to a safe,valid random choice rather than crashing.

**g. Testing Behavior with Missing or Invalid Keys (test_missing_key_in_json)**
Goal:
Ensure that the AI can handle unexpected or invalid keys in its previous move history without failing.

Method used:
Manually set ai.prev_moves to an invalid value such as "x", which does not exist in the transition matrix.
Call prediction() and assert that the returned move is still valid.

Why:
This simulates corrupted data or malformed previous-move sequences.
The expected behavior is that the AI should not crash and should default to a safe random move.

**h. Testing Multi-Round Learning Stability (test_multi_round_learning) FROM test_integration.py**
Goal:
Confirm that the multi-model system learns correctly over repeated rounds and that no model enters an invalid state.

Method used:
Create a temporary JSON file to store transition data.
Initialize a Multi_RPS_AI instance using this file.
Simulate a repeated pattern like r then p for 40 cycles, updating both transitions and scores.
Retrieve the best-performing model after learning.
Check that its prediction produces a valid move.

Why:
This ensures that long-term learning produces stable and valid output, and that the system does not break even when subjected to extended repetitive patterns.


**Coverage Report Analysis**
To evaluate how through my tests were, I used the Python coverage tool.
The entire project contains 268 executable lines, out of which 101 lines were not executed, bringing coverage to 62%. The number seems like it is on the lower end, but the reason is given at file no 5.

**Breakdown File by File**

**1. ai_code.py- 100% coverage**
All 47 statements were executed during testing. This shows that every branch of the prediction logic,score updating and model selection logic is covered by unit tests.

**2. move_storage.py- 88%**
The untested lines correspond to rarely triggered edge cases such as conditions that only occur when storage files are corrupted,and do no affect normal gameplay.

**3. test files(test_single_ai.py,test_multi_ai.py,test_edgecases.py)**
All of these files have above 94% coverage,with 2 files having 100%. This shows that the tests themselves executed fully.High coverage in the multi-model tests shows strong testing of the Markov chain models.

**4. test_integration.py - 95%coverage.**
Only 1 line was not executed. This could be due to an error path that is intentionally hard to trigger, such as unexpected I/O failures during integration testing.

**5. distutils hack file - 5% coverage****
This is the file that brings down the overall average. This file is an automatically installed library file and is **NOT PART OF THE PROJECT**. So the low coverage does not affect the correctness of the other tests.

**Conculsion**
Excluding the hack file, the overall coverage is extremely strong. All core components are thoroughly been tested. The few lines that are untested relate only to non-essential edge cases, and do not have a huge impact on the main functionality of the overall project.
