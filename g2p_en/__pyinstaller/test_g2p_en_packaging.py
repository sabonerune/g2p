import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

pyi_main = pytest.importorskip("PyInstaller.__main__")
is_module_satisfies = pytest.importorskip("PyInstaller.utils.hooks").is_module_satisfies

_pathsep = os.pathsep if is_module_satisfies("PyInstaller < 6") else ":"


def test_pyi_g2p_en(tmp_path: Path):
    appname = "app"
    nltk_data_path = "resources/nltk_data"
    cmudict_path = "corpora/cmudict"
    tagger_path = "taggers/averaged_perceptron_tagger_eng"

    app_file = tmp_path / f"{appname}.py"
    work_dir = tmp_path / "build"
    dist_dir = tmp_path / "dist"
    nltk_dir = tmp_path / nltk_data_path
    exe_dir = dist_dir / appname
    subprocess.run(
        [
            sys.executable,
            "-c",
            f"from g2p_en.g2p import download_data;download_data('{nltk_dir.as_posix()}')",
        ],
        check=True,
    )
    code = textwrap.dedent(
        f"""
        from pathlib import Path

        from g2p_en import G2p

        nltk_data = Path(__file__).parent / "{nltk_data_path}"


        def main():
            g2p = G2p(str(nltk_data))
            assert g2p("This is g2p test") == [
                "DH",
                "IH1",
                "S",
                " ",
                "IH1",
                "Z",
                " ",
                "G",
                "AH0",
                "T",
                "W",
                "AA1",
                "P",
                " ",
                "T",
                "EH1",
                "S",
                "T",
            ]


        if __name__ == "__main__":
            main()
        """
    )
    app_file.write_text(code)

    args = [
        "--workpath",
        str(work_dir),
        "--distpath",
        str(dist_dir),
        "--specpath",
        str(tmp_path),
        "--add-data",
        f"{nltk_dir / cmudict_path}{_pathsep}{nltk_data_path}/{cmudict_path}",
        "--add-data",
        f"{nltk_dir / tagger_path}{_pathsep}{nltk_data_path}/{tagger_path}",
        str(app_file),
    ]
    pyi_main.run(args)

    subprocess.run([str(exe_dir / appname)], check=True)
