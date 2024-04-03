import numpy as np
import pandas as pd
def raw_meas_to_csv(meas,freqs,angles,filename):
    meas = np.array(meas)
    meas_reshaped = meas.transpose(1,0,2).reshape(len(freqs),np.shape(angles)[0]*2)
    columns = []
    for angle in angles:
        columns.append(f're_{angle}')
        columns.append(f'im_{angle}')
    df = pd.DataFrame(meas_reshaped,columns=columns,index=freqs)

    df.to_csv(filename,index_label='freqs')
    return df

def format_raw_meas(meas,freqs,angles,filename):
    meas_rect = np.array(meas)
    meas_pol = []
    for meas_ang in meas_rect:
        meas_pol_tmp = []
        for meas_freq in meas_ang:
            mag = 20*np.log10(np.sqrt(meas_freq[0]**2+meas_freq[1]**2))
            phase = (np.arctan2(meas_freq[1],meas_freq[0])*180/np.pi)
            meas_pol_tmp.append([mag,phase])
        meas_pol.append(meas_pol_tmp)
    meas_pol = np.array(meas_pol)
    meas_pol_reshaped = meas_pol.transpose(1,0,2).reshape(len(freqs),np.shape(angles)[0]*2)
    columns =[]
    for angle in angles:
        columns.append(f'mag_{angle}')
        columns.append(f'phase_{angle}')

    
        
    df = pd.DataFrame(meas_pol_reshaped,columns=columns,index=freqs)
    df.to_csv(filename,index_label='freqs')


    

