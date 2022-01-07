# Probeserver Docker Container
This Docker container facilitates experimenting researching the self-healing capabilities afforded by Kubernetes to help manage issues encountered during the pod lifecycle.
This container can be coerced into doing the following through the use of environment variables.
- **CONTENT**: Customize what is returned in the response to a GET request made to the apex route.
- **CRASH_FACTOR**: Crash with a certain frequency on launch.
- **HEALTH_STATUS_FACTOR**: Cause the health status to periodically show a problem.
- **START_WAIT_SECS**: Pause for a specific amount of time before starting a web server.

A good reference for setting environments variables for containers can be found at the following link.

[Define Environment Variables for a Container](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/)

Additionally, the following functionality can be accessed via URLs served by the container's application server.
- **http://container.ip.address/crash**: Crash when a certain URL path is accessed.
- **http://container.ip.address/healthz**: Output health status when a certain URL path is accessed.
- **http://container.ip.address/resolve?service=service_name**: Resolve and make a request to a Kubernetes service hostname.

This container was built to accompany a blog post series detailing various caveats of managing the Kubernetes pod lifecycle. Please reference the following link for more specifics on how it is used.

[Preparing for and real-world Kubernetes Deployments Part 1](https://www.trek10.com/blog/preparing-for-and-real-world-kubernetes-deployments-part-2)
## Customize apex route response content
For the purposes of the blog post series this container was built for, configuring what the application server includes in its response was meant to provide a way to distinguish between different commits being deployed to a cluster. 
## Crash on launch
Configuring the container to crash with a certain frequency is meant to simulate a buggy container that made its way into a production environment. Definitely not unheard in today’s fast-paced agile development environments. 
## Alter health status output
I wanted a way to simulate a bad health check status within each pod. As such, I worked in a mechanism similar to what was used to crash the container outright into the health check endpoint to produce 500 status codes randomly in responses from the container’s application server.
## Delaying application server startup
Configuring the container to pause before starting an application server is meant to simulate the behavior of a production container taking a few seconds before being able to accept requests. 
## Crash on URL path
I wanted to create a way to crash the container at any point after the application server has started. The thought being that at some point I might want to get into some Chaos Testing for future POCs. Accessing the ‘/crash’ endpoint of the application server will achieve this result.
## Health status output
Kubernetes liveness and readiness probes require some form of health check. For the sake of simulating web applications, I configured the container’s application server to return a 200 status code and a brief JSON object when a request is made to the ‘/healthz’ endpoint to simulate an application’s (healthy) health check.
## Resolve and request a Kubernetes service
This feature is meant for researching Kubernetes proxy behavior and its effects on cross-availability zone traffic routing. This endpoint that facilitates this behavior takes in a hostname, resolves it, makes an HTTP (note: not secure HTTPS) request, and then outputs some information about the container servicing the request, the IP address of the resolved hostname, and the response provided by the remote service. A good way to test this is to run it against “checkip.dyndns.org”.
