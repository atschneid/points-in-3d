using ForwardDiff
using Plots
using PyCall

pushfirst!(PyVector(pyimport("sys")."path"), "")
pp = pyimport("plot_points")

# number of points to draw
n = 6

# number of iterations to run
iterations = 500

# maximum learning rate
max_alpha = .1/sqrt(n)

points = rand(n,2)

function spherical( a::Vector )
    return [cos(a[1])cos(a[2]),cos(a[1])sin(a[2]),sin(a[1])]
end

function cylindrical( a::Vector )
    return [cos(a[2]),sin(a[2]),a[1]]
end

function ellipsoid( a::Vector )
    return [2cos(a[1])cos(a[2]),cos(a[1])sin(a[2]),sin(a[1])]
end

function dist( a::Vector, b::Vector )
    return sum( (spherical(a).-spherical(b)).^2 )^.5
#    return sum( (cylindrical(a).-cylindrical(b)).^2 )^.5
#    return sum( (ellipsoid(a).-ellipsoid(b)).^2 )^.5 
end

function force( a::Vector, b::Vector )
    return dist(a,b)^-2
end


idx = 1
function force_sum(x::Vector)
    sum = 0
    for i in 1:n 
        if i != idx
	    sum += force(x,points[i,:])
	end
    end
    return sum
end

gradx = x -> ForwardDiff.gradient(force_sum, x)

println("points ", points[1,:]," ",points[2,:])
println("spherical ", spherical(points[1,:]),spherical(points[2,:]))

println("dist ", dist(points[1,:],points[2,:]))

println("force ", force(points[1,:],points[2,:]))
println("force_sum ", force_sum(points[1,:]))
println("gradx ", gradx(points[1,:]))


alpha = 0.0001
for iteration in 1:iterations
    global alpha *= 1.1
    global alpha = min(alpha,max_alpha)
    for i in 1:n
    	global idx = i
	grad = gradx(points[idx,:])
        points[idx,:] -= alpha * grad
    end
    if iteration % 50 == 0
        global idx = 1
	
        println(iteration, " alpha ", alpha )
    	println("points ", points[1,:]," ",points[2,:])
    	println("dist ", dist(points[1,:],points[2,:]))
	println("force ", force(points[1,:],points[2,:]))
        println("force_sum ", force_sum(points[1,:]))
        println("gradx ", gradx(points[idx,:]))

	carts = zeros(n,3)
        for i=1:n
    	    x,y,z = spherical(points[i,:])
            carts[i,:] = [x, y, z]
        end
	pp.plot_on_sphere( PyObject(carts),
			   save_file=PyObject(string(n,"plots",iteration,".png")),
			   tesselate=PyObject(true),
			   neighbors=PyObject(min(n,5)),
			   draw_sphere=PyObject(true))
   end
end