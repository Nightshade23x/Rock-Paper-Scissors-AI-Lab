This project contains two core AI components:

RPS_AI — a single-model Markov chain–based Rock Paper Scissors predictor. Since this component is no longer utilized, I have not talked about its tests below.

Multi_RPS_AI — a multi-model system that evaluates several RPS_AI models with different memory lengths and selects the best-performing one.This is the method I currentl use to predict the next move.

My unit tests were designed to verify the correctness of these components in a reproducible manner. The tests focus on transition storage, prediction accuracy, model selection, and functional correctness.

**a,b,c,d,e,f,g,h is from tests_multi_ai.py**

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

Goal: Ensure that update_scores() appends correct values of +1,-1 or 0 to all models,and ensures that the list represents the most recent game outcomes only.

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

**f.Testing handling of invalid previous moves(test_multi_handles_invalid_prev)**

Goal:Confirm that the system remains stable even if one of the RPS_AI models contains corrupted or invalid previous moves.

Method used:

Manually set one model's prev_moves to invalid values like ["x","y"]

Call get_move()

Verify that the returned move is still one of the valid moves(r,p or s)

Why:

The model must be robust.Even if one model enters a corrupted state, the system must continue to functioning and still produce legal moves.

**g.Testing score window enforcement(test_scores_trim_to_focus_length)**

Goal:Ensure that score histories do not grow large and will always respect the specified focus_length sliding window.

Method used:

Repeatedly call update_model_scores("r") nore times than the allowed focus_length.

Check that each model's score list is still equal to 5(which was the focus_length in my implementation)

Why:

The scoring system must maintain a fixed window of recent performance. This will ensure that outdated scores from influencing the selection of the best model in the gameplay.

**h. Testing Tie handling(test_best_ai_handles_ties)**

Goal:Ensure that best_ai() behaves correctly when 2 models end up having identical score totals.

Method used:

Manually assign equal score lists to 2 models.

Call best_ai

Ensure that the returned model is one of the tied models.

Why:

Tie scenarios are very possible in the gameplay. The AI must handle these scenarios and still return a valid model without any errors.


**i and j are both from test_edge_cases.py**


**i. Testing Prediction with Insufficient Previous Moves (test_empty_prev_moves)**

Goal:

Verify that the AI behaves correctly when there are fewer previous moves than the memory length requires.

Method used:

Create an RPS_AI model with memory_length=3, but do not provide enough moves to form a valid key.

Call prediction() and ensure the returned move is one of r,p or s.

Why:

If the AI does not have enough history to form a sequence key, it should fall back to a safe,valid random choice rather than crashing.

**j. Testing Behavior with Missing or Invalid Keys (test_missing_key_in_json)**

Goal:Ensure that the AI can handle unexpected or invalid keys in its previous move history without failing.

Method used:

Manually set ai.prev_moves to an invalid value such as "x", which does not exist in the transition matrix.

Call prediction() and assert that the returned move is still valid.

Why:

This simulates corrupted data or malformed previous-move sequences.

The expected behavior is that the AI should not crash and should default to a safe random move.

**k. Testing Multi-Round Learning Stability (test_multi_round_learning) FROM test_integration.py**

Goal: Confirm that the multi-model system learns correctly over repeated rounds and that no model enters an invalid state.

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

There are 178 statements to execute, and 3 were missed, bringing the overall coverage to approximately 98%.
Note,I did not include RPS_Game_Code.py because it is does not contribute to the AI logic and is simply just used to run the game.

**Breakdown File by File**

**1. ai_code.py- 100% coverage**

All 47 statements were executed during testing. This shows that every branch of the prediction logic,score updating and model selection logic is covered by unit tests.

**2. move_storage.py- 94%**

The untested lines correspond to rarely triggered edge cases such as conditions that only occur when storage files are corrupted,and do no affect normal gameplay.

**3. test files(test_single_ai.py,test_multi_ai.py,test_edgecases.py)**

All of these files have above 95% coverage,with 2 files having 100%. This shows that the tests themselves executed fully.High coverage in the multi-model tests shows strong testing of the Markov chain models.

**4. test_integration.py - 100%coverage.**

All of the lines were executed without any issues.This shows the integration logic is well covered by unittests.


**Conclusion**

My coverage results showcase that all core modules including scoring logic, move storage, multi model systems are all well tested.The remaining untested statements are due to very rare edge cases that have no impact on the day to day running of the program.The coverage score provides a strong confidence in the stability and reliability of the project.
