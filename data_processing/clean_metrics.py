from pathlib import Path
import pandas as pd


if __name__ == "__main__":
    # Process the Model and Resource Name
    curr_dir = Path.cwd()
    metrics_dir = curr_dir / "metrics"

    resource_model_lst = [path for path in metrics_dir.iterdir() if path.is_dir()]

    # Dictionary for storing dataframes
    df_dict: dict[str, pd.DataFrame] = {}

    for resource_model in resource_model_lst:
        name = resource_model.name
        cpu_gpu_type, model_name = name.split("-")[0], "-".join(name.split("-")[1:])
        exec_modes = [path for path in resource_model.iterdir() if path.is_dir()]
        for exec_mode_path in exec_modes:
            exec_mode = exec_mode_path.name

            for apps_path in exec_mode_path.iterdir():
                if not apps_path.is_dir():
                    continue
                app_name = apps_path.name.split("_")[0]

                csv_source = apps_path / f"{app_name}_metrics.csv"
                # Get the dataframe
                source_df = pd.read_csv(csv_source)

                # Create Intermediate DataFrame
                aug_source_df = source_df.copy()
                aug_source_df["model_name"] = model_name
                aug_source_df["test_resource"] = cpu_gpu_type
                aug_source_df["exec_mode"] = exec_mode

                if app_name in df_dict:
                    df_dict[app_name] = pd.concat(
                        [df_dict[app_name], aug_source_df], ignore_index=True
                    )
                else:
                    df_dict[app_name] = aug_source_df.copy()

    for df_name in df_dict:
        df_dict[df_name].to_csv(f"./{df_name}.csv", index=False)
