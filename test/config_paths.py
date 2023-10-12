import platformdirs

appname = "OurGreatApp"
print(f"User config files should be stored in {platformdirs.user_config_dir(appname)}")
print(f"User logs should be stored in {platformdirs.user_log_dir(appname)}")
