## Configuation

The configuration file is located im the `./cfg/` subdirectory. It is a JSON file.

### Keys
#### "map":
- **"mapbox_api_key":**  some Mapbox styles require an api key. This value is passed to the `scatter_mapbox()` method for the base map layout.
- **"mapbox_style":** URL for custom Mapbox design. This value is passed to the `scatter_mapbox()` method for the base map layout.
- **"dashboard_name":** filename to be used when chart is pushed to the Plotly hosting service.
- **"starting_point":** starting point of the route to be mapped. This was designed with cities in mind, but could represent any geographic point.
- **"ending_point":** ending point of the route to be mapped.
- **"site_css":** colors and fonts to be used in the map. Designed with the idea of embedding into an existing website. **NOTE**: The keys `heading` and `paragraph` are explicitly referenced in the runtracker.py script and should not be changed.

#### "mySQL":
- **"connection_config":**: connection credentials to a mySQL database.
- **insert_tables:** table that mileage data retrieved from the Google Fit API will be inserted into. User can specify a "dev" table that can be used for testing. The value for `"insert_tables": "prod"` should be the same table as `"data_tables": "run_data"`.
- **"data_tables":** dictionary indicating which tables in the database contain relevant types of data.
    - **"map_data":** must contain the latitude and longitude of each point on the route to be mapped, and also a column showing the cumulative distance on the route covered at each point.
    - **"run_data":** contains mileage data per day. 
    - **"poi_data":** contains latitude, longitiude, and text label for each "point of interest" to be mapped along the route. POIs are entirely up to the individual user.

#### "google_fit_api":
- **"secrets_file":** JSON file generated by Google when app is authorized. Must be located in `./cfg/` folder.
- **"token_file":** JSON file generated by Google when OAuth2 credentials are generated. Must be located in `./cfg/` folder.