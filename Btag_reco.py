from pathlib import Path
#import argparse

import basf2 as b2
import modularAnalysis as ma

# Necessary to run argparse
#from ROOT import PyConfig
#PyConfig.IgnoreCommandLineOptions = 1  # noqa

#from ROOT import Belle2

import stdPhotons
from stdCharged import stdMostLikely
# from stdPhotons import stdPhotons
from variables import variables as vm

from BtagFeatureSaverModule import BtagFeatureSaverModule
import fei




def FEI_graphs_path(outputfile, inputs, isMC=True): 


    # This assumes one input file only
    # Use this to set the output filenames to match the input

    path = b2.create_path()
    b2.conditions.prepend_globaltag('analysis_tools_light-2205-abys')
    ma.inputMdst(inputs, path=path)

    # ###### USING THE FEI SKIM RECONSTRUCTION #######
    # This is from https://stash.desy.de/projects/B2/repos/software/browse/skim/scripts/skim/fei.py?at=release-04-02-04
    # These are event-level selections intended to filter down evets
    # We use these to make this a fair comparison with the FEI
#    lcareco  = LCARecoModule('B+:feiHadronic', 'output.hdf5')
#    path.add_module(lcareco)
    configuration = fei.config.FeiConfiguration(prefix='FEIv4_2022_MC15_light-2205-abys', training=False, monitor=False)
    particles = fei.get_default_channels(baryonic=True)
    feistate = fei.get_path(particles, configuration)
    path.add_path(feistate.path)
    path.add_module('MCMatcherParticles', listName='B+:generic', looseMCMatching=True)

    save  = BtagFeatureSaverModule('B+:generic',['extraInfo(SignalProbability)','abs(PDG)','charge', 'dM','M', 'chiProb', 'dr', 'dz', 'E','px','py','pz','useCMSFrame(p)','useCMSFrame(pt)', 'useCMSFrame(pz)', 'useCMSFrame(phi)', 'useCMSFrame(theta)', 'useCMSFrame(E)' ], outputfile)
    path.add_module(save)

    # Actually run everything
    return path
