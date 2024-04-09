# iharp-pure-query

Run `init_venv.sh` to initialize virtual environment and install packages. 
```bash
bash init_venv.sh
```

To see the query examples, open jupyter notebook `src/example.ipynb` and run all cells. 

To run tests, run `pytest` in terminal. 
```bash
pytest
```

## Roadmap

| Query                              |    Single File     |    Multi Files     | Files + API | pre-aggregation | pre-aggregation + API |
| ---------------------------------- | :----------------: | :----------------: | :---------: | :-------------: | :-------------------: |
| single value aggregation           | :white_check_mark: | :white_check_mark: |             |                 |                       |
| time series aggregation            | :white_check_mark: | :white_check_mark: |             |                 |                       |
| heatmap aggregation (single layer) | :white_check_mark: | :white_check_mark: |             |                 |                       |
| heatmap aggregation (multi layer)  | :white_check_mark: | :white_check_mark: |             |                 |                       |
| value-criteria query               | :white_check_mark: | :white_check_mark: |             |                 |                       |
| arbitrary shape query              |                    |                    |             |                 |                       |
| time period finding                |                    |                    |             |                 |                       |
| area finding                       | :white_check_mark: | :white_check_mark: |             |                 |                       |
