import sys
import numpy as np
import matplotlib.pyplot as plt

# define IndexTracker class to map events and scores
class ScoringPanel(object):
    def __init__(self, fig, ax, X, Y, cell_label,timestamp,start_ind): #added cell label and time stamp here
        self.fig = fig
        self.ax = ax
        self.X = X
        self.Y = Y
        self.cell_label = cell_label #adding the cell label
        self.ind = start_ind
        self.col_dict = {0:'r', 1:'k', 2:'b'}
        self.quality_labels = ['PN', 'FP', 'NE', 'BE'] #adding label of NE- 'nice event', BE -'not so nice event', FP - 'false positive', PN - 'pure noise'
        self.minitype_labels = ['AMPA', 'NMDA' ] #to add label of AMPA or NMDA if needed
        self.event_labels = np.array([self.quality_labels[0]] * Y.shape[0]) #to store the updated quality label
        self.type_labels = np.array([self.minitype_labels[0]] * Y.shape[0]) #to store the updated minitype label
        self.timestamp = timestamp #timestamp
        self.update()

        

    # Use mouse to change event
    def onscroll(self, event):
        if event.button == 'up':
            self.ind = (self.ind + 1)
        else:
            self.ind = (self.ind - 1)
        self.update()

    # Use keyboard to change events and scores
    def onclick(self, event):
        #print('press', event.key) ### Can be used to show key bindings
        sys.stdout.flush()
        if event.key == 'right':
            self.ind = (self.ind + 1)
        elif event.key == 'left':
            self.ind = (self.ind - 1)
        if event.key == 'm':
            self.Y[self.ind] = (self.Y[self.ind]+1)%3
        elif event.key == 'k': #if you press the key 'k', you can change the 'quality label' of that datastretch as FP, PN, NE or BE
            current_quality_index = (self.quality_labels.index(self.event_labels[self.ind]) + 1) % len(self.quality_labels)
            self.event_labels[self.ind] = self.quality_labels[current_quality_index]
        elif event.key == 'i': #if you press the key 'i', you can change the 'minitype label' of that datastretch as AMPA or NMDA
            current_type_index = (self.minitype_labels.index(self.type_labels[self.ind]) + 1) % len(self.minitype_labels)
            self.type_labels[self.ind] = self.minitype_labels[current_type_index]
        self.update()



    def update(self):
        self.ax.clear()
        
        # Take care of boundary indices
        if self.ind < 0:
            self.ind += self.Y.shape[0]
        elif self.ind >= self.Y.shape[0]:
            self.ind = self.ind - self.Y.shape[0]
        
    
        self.ax.plot(self.timestamp[self.ind],self.X[self.ind], c=self.col_dict[self.Y[self.ind]]) #to plot the timestamp of the datastretch in the x-axis
        self.ax.set_ylim(-40, 20) #to keep the Y-axis constant when plotting the extracted datastretches
        self.ax.set_ylabel('# %s' % self.ind)
        self.ax.set_title(f'label: {self.Y[self.ind]}, cell: {self.cell_label[self.ind]}, quality: {self.event_labels[self.ind]}') #added plotting the cell-label, quality label and the minitype label
        self.fig.canvas.draw_idle()