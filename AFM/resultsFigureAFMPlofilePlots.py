"""
@author: DjimDeRidder
"""
import pandas as pd
import os

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib_scalebar.scalebar import ScaleBar

excelNameI = "height2.xlsx"
excelNameP = "profilePlots.xlsx"
imageSheetA = "1116_004"
imageSheetB = "1027_957"
profileSheetA = "profileA"
profileSheetB = "profileB"
coordSheetA = "coordA"
coordSheetB = "coordB"
absolute_path_I = os.path.join(os.getcwd(), 'input', excelNameI)
absolute_path_P = os.path.join(os.getcwd(), 'input', excelNameP)

"import image"
IA= pd.read_excel(absolute_path_I, sheet_name=imageSheetA).to_numpy()*10**9
IB= pd.read_excel(absolute_path_I, sheet_name=imageSheetB).to_numpy()*10**9
"average height of membrane found with mainFindHeight"
mubgA =7.67138527 #expected = (7.3,2,0.2,13,5,0.03)
mubgB = 8.03530654; #expected = (7.45,3,0.1,16,5,0.075)
"import profile plots and coordiantes"
profileA = pd.read_excel(absolute_path_P, sheet_name=profileSheetA).to_numpy()*10**9#-mubgA
coordA = pd.read_excel(absolute_path_P, sheet_name=coordSheetA).to_numpy()
profileB = pd.read_excel(absolute_path_P, sheet_name=profileSheetB).to_numpy()*10**9#-mubgB
coordB = pd.read_excel(absolute_path_P, sheet_name=coordSheetB).to_numpy()

fig = plt.figure(tight_layout=True)
fig.set_size_inches(12,9)
gs2 = gridspec.GridSpec(4, 2,width_ratios=[1,1],height_ratios=[3,1,1,1])
ax1 = fig.add_subplot(gs2[0, 0])
ax2 = fig.add_subplot(gs2[0, 1])
ax3 = fig.add_subplot(gs2[1, 0]) 
ax4 = fig.add_subplot(gs2[1, 1])
ax5 = fig.add_subplot(gs2[2, 0]) 
ax6 = fig.add_subplot(gs2[2, 1])
ax7 = fig.add_subplot(gs2[3, 0]) 
ax8 = fig.add_subplot(gs2[3, 1])

cax1=ax1.imshow(IA,'afmhot')
cax1.set_clim(0, 35)
ax1.axis('off')
scalebar = ScaleBar(3000/IA.shape[1], "nm",length_fraction=0.3,width_fraction=1/30,color='w',frameon=False,location='lower left',label_formatter = lambda x, y:'')
ax1.add_artist(scalebar)
cbar1 = plt.colorbar(cax1, ax=ax1,shrink=0.75,ticks=[0,35])
cbar1.set_ticklabels(["0 nm", "35 nm"])
cbar1.ax.tick_params(labelsize=15)
for i in range(coordA.shape[0]):
    ax1.plot([coordA[i,1], coordA[i,3]], [coordA[i,2], coordA[i,4]],'w',linewidth=2)
    #ax1.text((coordA[i,1]+coordA[i,3])/2+10,(coordA[i,2]+coordA[i,4])/2,s=str(i+1), c='w',fontsize=12)
    

cax2=ax2.imshow(IB,'afmhot')
cax2.set_clim(0, 35)
ax2.axis('off')
scalebar = ScaleBar(3000/IA.shape[1], "nm",length_fraction=0.3,width_fraction=1/30,color='w',frameon=False,location='lower left')
ax2.add_artist(scalebar)
cbar2 = plt.colorbar(cax2, ax=ax2,shrink=0.75,ticks=[0,35])
cbar2.set_ticklabels(["0 nm", "35 nm"])
cbar2.ax.tick_params(labelsize=15)
for i in range(coordA.shape[0]):
    ax2.plot([coordB[i,1], coordB[i,3]], [coordB[i,2], coordB[i,4]],'w',linewidth=2)
    #ax2.text((coordB[i,1]+coordB[i,3])/2+10,(coordB[i,2]+coordB[i,4])/2,s=str(i+1), c='w',fontsize=12)
    
line1, = ax3.plot(profileA[:,0],profileA[:,1],'k',linewidth=2,label='profile 1')
line2, = ax3.plot(profileA[:,2],profileA[:,3],'c',linewidth=2,label='profile 2')
line3, = ax3.plot(profileA[:,4],profileA[:,5],'m',linewidth=2,label='profile 3')
ax3.set_xlabel('x [nm]',fontsize=15)
ax3.set_ylabel('Height [nm]',fontsize=15)
ax3.legend(handles=[line1, line2, line3],fontsize=12)
ax3.set_ylim([0, 30])

line1, = ax4.plot(profileB[:,0],profileB[:,1],'k',linewidth=2,label='profile 1')
line2, = ax4.plot(profileB[:,2],profileB[:,3],'c',linewidth=2,label='profile 2')
line3, = ax4.plot(profileB[:,4],profileB[:,5],'m',linewidth=2,label='profile 3')
ax4.set_xlabel('x [nm]',fontsize=15)
ax4.set_ylabel('Height [nm]',fontsize=15)
ax4.legend(handles=[line1, line2, line3],fontsize=12)
ax4.set_ylim([0, 30])

line4, = ax5.plot(profileA[:,6],profileA[:,7],'k',linewidth=2,label='profile 4')
line5, = ax5.plot(profileA[:,8],profileA[:,9],'c',linewidth=2,label='profile 5')
line6, = ax5.plot(profileA[:,10],profileA[:,11],'m',linewidth=2,label='profile 6')
ax5.set_xlabel('x [nm]',fontsize=15)
ax5.set_ylabel('Height [nm]',fontsize=15)
ax5.legend(handles=[line4, line5, line6],fontsize=12)
ax5.set_ylim([0, 30])

line4, = ax6.plot(profileB[:,6],profileB[:,7],'k',linewidth=2,label='profile 4')
line5, = ax6.plot(profileB[:,8],profileB[:,9],'c',linewidth=2,label='profile 5')
line6, = ax6.plot(profileB[:,10],profileB[:,11],'m',linewidth=2,label='profile 6')
ax6.set_xlabel('x [nm]',fontsize=15)
ax6.set_ylabel('Height [nm]',fontsize=15)
ax6.legend(handles=[line4, line5, line6],fontsize=12)
ax6.set_ylim([0, 30])

line7, = ax7.plot(profileA[:,12],profileA[:,13],'k',linewidth=2,label='profile 7')
line8, = ax7.plot(profileA[:,14],profileA[:,15],'c',linewidth=2,label='profile 8')
line9, = ax7.plot(profileA[:,16],profileA[:,17],'m',linewidth=2,label='profile 9')
ax7.set_xlabel('x [nm]',fontsize=15)
ax7.set_ylabel('Height [nm]',fontsize=15)
ax7.legend(handles=[line7, line8, line9],fontsize=12)
ax7.set_ylim([0, 30])

line7, = ax8.plot(profileB[:,12],profileB[:,13],'k',linewidth=2,label='profile 7')
line8, = ax8.plot(profileB[:,14],profileB[:,15],'c',linewidth=2,label='profile 8')
line9, = ax8.plot(profileB[:,16],profileB[:,17],'m',linewidth=2,label='profile 9')
ax8.set_xlabel('x [nm]',fontsize=15)
ax8.set_ylabel('Height [nm]',fontsize=15)
ax8.legend(handles=[line7, line8, line9],fontsize=12)
ax8.set_ylim([0, 30])

dirName = os.path.join(os.getcwd(), 'output', 'resultsProfilePlotAFM.png');
fig.savefig(dirName, format='png', dpi=720)