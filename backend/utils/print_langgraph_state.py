def print_state(state: dict):
    print("\n===== CURRENT STATE =====\n")
    
    for key, value in state.items():
        print(f"{key}:")
        if key=="visualization_base64":
            continue
        if key == "pandas_dataframe":
            try:
                print(f"  DataFrame shape: {value.shape}")
                print(f"  Columns: {list(value.columns)}")
                print(f"  Preview:\n{value.head(3)}")
            except Exception:
                print("  Unable to display DataFrame")

        elif isinstance(value, dict):
            print(f"  {value}")

        else:
            print(f"  {value}")
        
        print("\n------------------------\n")