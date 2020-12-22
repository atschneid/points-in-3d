import sys
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

epsilon = 1e-1

# def spherical_to_cartesian( theta, phi, r=1 ):
#     return [ (r * np.cos( t ) * np.cos( p ),
#               r * np.cos( t ) * np.sin( p ),
#               r * np.sin( t ) ) for (t,p) in zip( theta, phi ) ]
    
def distance( x, y, l2=True ):
    x = np.array( x ); y = np.array( y )
    return np.sqrt( np.sum( np.array( x-y )**2 ) )

def plot_on_sphere( coords, label=None, save_file=None, tesselate=False, neighbors='auto', show=False, draw_sphere=False ):

    coords = np.array( coords )
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    if draw_sphere:
        # Create a sphere
        phi, theta = np.mgrid[0.0:np.pi:100j, 0.0:2.0*np.pi:100j]
        x = np.sin(phi)*np.cos(theta)
        y = np.sin(phi)*np.sin(theta)
        z = np.cos(phi)

        ax.plot_surface( x,y,z, rstride=1, cstride=1, color='c', alpha=0.3, linewidth=1.0)

    for (x,y,z) in coords:
        ax.scatter(x,y,z,color="k",s=20)
        ax.plot( (0,x),(0,y),zs=(0,z), color='green', linestyle='dashed', linewidth=1 )

    if tesselate:
        distances = np.zeros( (len( coords ), len( coords )) )
        print( 'building distances for tesselation...' )
        for i in range( len( coords ) ):
            for j in range( i ):
                distances[i,j] = distance( coords[i], coords[j] )
        distances += distances.T
        print( 'done' )

        for i in range( len( coords ) ):
            (x1,y1,z1) = coords[i]
            nn_ids = np.argsort( distances[i] )

            if neighbors == 'auto':
                nns = []
                for j, j_arg in enumerate( nn_ids ):
                    if j == 0:
                        continue
                    nns.append( (coords[ j_arg ], distances[i,j_arg]) )
                    if len( coords ) > j+1 and distances[i,nn_ids[j+1]] - distances[i,j_arg] > epsilon:
                        break
            else: # neighbors == some int val
                neighbors = min( len( nn_ids ) - 1, int( neighbors ) )
                nns = zip( coords[ nn_ids[1:neighbors+1] ], distances[i,nn_ids[1:neighbors+1]] )

            d_avg = []
            for nn in nns:
                (x2,y2,z2) = nn[0]
                d_avg += [nn[1]]
                ax.plot( (x1,x2),(y1,y2),zs=(z1,z2), color='red', linewidth=1 )
            print( 'point : ', i, ' distance avg : ', d_avg, np.mean( d_avg ), np.std( d_avg ) )


    if label != None:
        ax.set_title( label )

    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    ax.set_zlim([-1,1])

    plt.tight_layout()
    if save_file is not None:
        plt.savefig( save_file )

    if show is True:
        plt.show()

    plt.close()

    
def main_fn(num_points):

    random_points = 1 - 2 * np.random.rand( num_points, 3 )
    normed_random_points = [ (a,b,c) / np.sqrt( a**2 + b**2 + c**2 ) for (a,b,c) in random_points ]
    print( normed_random_points )

    plot_on_sphere( normed_random_points, show=True )



if __name__ == "__main__":
    # execute only if run as a script
    if len(sys.argv) > 1:
        main_fn(int(sys.argv[1]))
    else:
        main_fn(10)
