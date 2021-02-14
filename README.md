# TeamCodeAPI
Backend server for teamcodes

# Endpoints:
- **/addteam**:
    - Methods: Post
    - input: team_code, user_id
    -output: error: error message/success
- **/jointeam**:
    - Methods: Post
    - input: team_code, user_id
    - output: error: error message/success
- **getTeamInfo/<team_code>**:
    - Methods: Get
    - input: team_code
    - output: - error: error message/success
        - owner: owner user id
        - members: array of user ids
