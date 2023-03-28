from glob import glob
import json
import multiprocessing
import os
import subprocess
from typing import Tuple
import random
from typing import Any, Dict
import yaml
import b2luigi as luigi
import basf2
from b2luigi.basf2_helper import Basf2nTupleMergeTask, Basf2PathTask
from inclusivebtoxlv.batch_tools import read_file_dict, scan_mdst_files
import modularAnalysis as ma
from root_numpy import list_trees
import root_pandas
from feicalib import Xsll_path
from Btag_reco import FEI_graphs_path
results_path
log_path
luigi.set_setting(
    "result_dir",
    "results_path",
)
luigi.set_setting(
    "log_dir", "log_path"
)
luigi.set_setting("batch_system", "htcondor")
luigi.set_setting("executable", ["python3"])
luigi.set_setting("env_script", "setup_local_sll.sh")

basf2.add_module_search_path(".")

output_files = ['features.hdf5']
class AnalysisTask(Basf2PathTask):
    max_event = 30000
    htcondor_settings = {
        "+requestRuntime": 36000
        }
    
    input_files = luigi.Parameter(hashed=True)
    feiHadronicBzero = luigi.BoolParameter(default=False)
    feiHadronicBplus = luigi.BoolParameter(default=False)

    def create_path(self):
        file_with_path = self.get_output_file_name(output_files[0])
        path = basf2.create_path()
        path.add_module("EnableMyVariable")
        print("Input files ", self.input_files)
        self.path = FEI_graphs_path(
                file_with_path,
                self.input_files[0],
                isMC=True
            )
        path.add_path(self.path)
        return path

    def output(self):
        self.output_files = output_files
        for f in output_files:
            yield self.add_to_output(f)



class AnalysisWrapperTask(luigi.WrapperTask):
    file_dict = luigi.Parameter(hashed=True)
    feiHadronicBzero = luigi.BoolParameter()
    feiHadronicBplus = luigi.BoolParameter()

    @staticmethod
    def generate_chunks(seq, chunk_size=1):
        return [seq[i : i + chunk_size] for i in range(0, len(seq), chunk_size)]

    def requires(self):

        file_dict = read_file_dict(self.file_dict)
        files_to_process = [
            filename for filename, attrs in file_dict.items() if attrs["nevents"] > 0
        ]

        for chunk in self.generate_chunks(files_to_process, chunk_size=1):
            yield AnalysisTask(
                feiHadronicBzero=self.feiHadronicBzero,
                feiHadronicBplus=self.feiHadronicBplus,
                input_files=chunk
            )


class MasterTask(luigi.WrapperTask):
    def requires(self):
        file_dict_dir = ""

        file_dict = os.path.join(file_dict_dir, f"Bfei_ch.json")
        yield AnalysisWrapperTask(
                    file_dict=file_dict,
                    feiHadronicBzero=True,
                    feiHadronicBplus=True,
                )


if __name__ == "__main__":
    luigi.process(MasterTask(), workers=10000, batch=True)
