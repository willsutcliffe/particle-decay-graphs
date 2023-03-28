import basf2 as b2
from ROOT import Belle2
from variables import variables as vm
import h5py
import numpy as np


class BtagFeatureSaverModule(b2.Module):
    ''' Save given features of given particles lists '''

    def __init__(
        self,
        particle_list,
        features,
        output_file,
    ):
        ''' Class Constructor.

        Args:
            particle_lists (list): Name of particle lists to save features of
            features (list): List of features to save for each particle
            b_parent_var (str): Name of variable used to flag ancestor B meson and split particles
            output_file (str): Path to output file to save
        '''
        super().__init__()
        self.particle_list = particle_list
        self.features = features
        self.output_file = output_file

    def initialize(self):
        '''Create a member to access event info StoreArray '''
        self.eventinfo = Belle2.PyStoreObj('EventMetaData')

        # Create the output file, fails if exists
        self.h5_outfile = h5py.File(self.output_file, 'w-')

        # Save the list of feature names (want to know their order)
        self.h5_outfile.attrs['features'] = self.features

    def event(self):
        ''' Run every event '''

        # Event number from EventMetaData -loaded with PyStoreObj
        evt_num = self.eventinfo.getEvent()

        # Where we'll append features
        # Ideally this would be saved in evt_feat_dict but the -1 for unmatched
        # particles messes that up

        # IMPORTANT: The ArrayIndex is 0-based.
        # mcplist contains the root particles we are to create LCAs from

            # Get the particle list (note this is a regular Particle list, not MCParticle)
        p_list = Belle2.PyStoreObj(self.particle_list)
        Btag = 0
        for part in p_list.obj():
            # only store 10% of fakes currently to save space
            isSignal = vm.evaluate('isSignal',part) 
            if np.isnan(isSignal) == 0 and ( np.random.uniform(0,1,1)[0] < 0.005 or isSignal == 1 ):
                array_index = part.getArrayIndex()
                #print('Evt num ', evt_num, 'Btag ', array_index)
                self.node_dict = {
            #'indices': [],
            'ndaughters': [],
            #'pdgs': []
             }

                self.evt_feats = []

                # Store key node
                self.evt_feats.append([vm.evaluate(f, part) for f in self.features])
                #self.node_dict['pdgs'].append(part.getPDGCode())
                self.node_dict['ndaughters'].append(part.getNDaughters())
                #self.node_dict['indices'].append(array_index)

                # Store rest of tree B, B_daughters, First_B_daughter_daughters
                self.store_features(part)
                dset = self.h5_outfile.create_dataset(f'{evt_num}/{Btag}', data=self.evt_feats)
                #dset.attrs['indices'] = self.node_dict['indices']
                dset.attrs['ndaughters'] = self.node_dict['ndaughters']
                #dset.attrs['pdgs'] = self.node_dict['pdgs']
                dset.attrs['isSignal'] = vm.evaluate('isSignal',part)
                dset.attrs['Mbc'] = vm.evaluate('Mbc',part)
                #print(vm.evaluate('isSignal',part))
                Btag = Btag + 1


    def store_features(self, part):
        for dau in part.getDaughters():
            array_index = dau.getArrayIndex()
            self.evt_feats.append([vm.evaluate(f, dau) for f in self.features])
            #self.node_dict['pdgs'].append(dau.getPDGCode())
            self.node_dict['ndaughters'].append(dau.getNDaughters())
            #self.node_dict['indices'].append(array_index)
        for dau in part.getDaughters():
            self.store_features(dau)

        

    def terminate(self):
        ''' Called once after all the processing is complete'''
        self.h5_outfile.close()
