from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("g2p_en", includes=["checkpoint20.npz", "homographs.en"])
