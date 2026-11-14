# Containers 101: the exercise

You put a small web app in a container.
You write a Dockerfile, you build an image, and you run a container.
The app shows a picture of a cat.

- Time: about 30 minutes
- You do not need to know Python

The steps have the same numbers as the steps on the slides.

## The app

You get the folder `hello-web`. It contains the files `app.py` and `luci-sitting.png`.

`app.py` is a small web app. It shows the picture `luci-sitting.png`. Do not change it.

## Step 1: Download Docker

You need Docker on your machine.

- Mac or Windows: install Docker Desktop from <https://www.docker.com/products/docker-desktop/>. Then start it.
- Linux: install Docker Engine.

Podman works too. If you use Podman, write `podman` in place of `docker` in each command.

Make sure that Docker runs:

```bash
docker version
```

The output must show a `Client` part and a `Server` part.
If the `Server` part shows an error, start Docker Desktop and wait until it is ready.

## Step 2: Set up Docker in your IDE (optional)

You can skip this step. A terminal and a text editor are sufficient for this exercise.

Open a terminal in the folder `hello-web`.

## Step 3: Write the Dockerfile

Make a file with the name `Dockerfile` in the folder `hello-web`, next to `app.py`.
The name has no extension. `Dockerfile.txt` does not work.

The file must do five things. Write one instruction on each line.

| # | The file must do this | Instruction |
|---|---|---|
| 1 | Start from the image `python:3.14-slim` | `FROM` |
| 2 | Use the folder `/app` inside the image | `WORKDIR` |
| 3 | Copy `app.py` and `luci-sitting.png` into the image | `COPY` |
| 4 | Record that the app listens on port 8000 | `EXPOSE` |
| 5 | Run `python app.py` when a container starts | `CMD` |

If you cannot continue, ask for the slide that shows the Dockerfile.

## Step 4: Build the image

```bash
docker build -t hello-web:1.0 .
```

Do not forget the dot at the end.

- `-t hello-web:1.0` gives the image a name and a tag.
- The dot tells Docker to use the files in this folder.

The first build downloads the base image: 44 MB. Later builds are faster.
A good build has no line with the word `ERROR`.

Check the result:

```bash
docker images hello-web
```

The command shows one image with the tag `1.0`.

## Step 5: Run the container

```bash
docker run -d --name hello -p 8080:8000 hello-web:1.0
```

- `-d` runs the container in the background.
- `--name hello` gives the container a name.
- `-p 8080:8000` connects port 8080 of your machine to port 8000 of the container.

Open this address in your browser: <http://localhost:8080>

You see the picture of the cat. The line below the picture gives the ID of your container.

If the page says that the file `luci-sitting.png` is not in the container, your `COPY` line did not copy the picture.
Correct the Dockerfile, build again, remove the container with `docker rm -f hello`, and run again.

## Step 6: Look at the container

```bash
docker ps
```

This command lists the containers that run. You see `hello`.

```bash
docker logs hello
```

This command shows the output of the app. Each page load adds lines.

```bash
docker stop hello
```

This command stops the container. Load the page again: it is gone.

```bash
docker rm hello
```

This command removes the container. The image stays on your machine.
The command from step 5 starts a new container from the same image.

## If you finish early

Start the container again with the command from step 5. Then try these tasks.

### 1. A second container from the same image

```bash
docker run -d --name hello-2 -p 8081:8000 hello-web:1.0
```

Open <http://localhost:8081>. Compare the container IDs on the two pages.
One image started two containers.

### 2. A look inside the container

```bash
docker exec -it hello sh
```

You are now inside the container. Try `ls`, `hostname`, `whoami`, and `cat /etc/os-release`.
Type `exit` to leave.

Then run this command on your machine. It shows that the container is one process.

```bash
docker top hello
```

### 3. A container has only the files that you copy

Change the `COPY` line so that it copies only `app.py`. Then build a second version and run it:

```bash
docker build -t hello-web:2.0 .
```

```bash
docker run -d --name hello-3 -p 8082:8000 hello-web:2.0
```

Open <http://localhost:8082>. What does the page say? Why?
Find the word `CACHED` in the output of the build. Which step ran again?

Change the `COPY` line back when you finish.

### 4. The layers of the image

```bash
docker history hello-web:1.0
```

Find the layer that your `COPY` instruction made. Find its size.

### 5. For experts

- Run the app as a user that is not root. Add `RUN useradd --create-home app` and `USER app` to the Dockerfile. Check with `docker exec hello whoami`.
- Write the last line as `CMD python app.py`, without the brackets. Build and run. Measure the time that `docker stop hello` takes. Explain the difference.
- Change the base image to `python:3.14-alpine`. Compare the sizes with `docker images`.

## When something fails

| The message says | Do this |
|---|---|
| `failed to connect to the docker API` or `Cannot connect to the Docker daemon` | Start Docker Desktop. Wait until it is ready. Try again. |
| `open Dockerfile: no such file or directory` | Give the file the name `Dockerfile`, not `Dockerfile.txt`. Make sure that your terminal is in the folder `hello-web`. |
| `'docker buildx build' requires 1 argument` | Put the dot at the end: `docker build -t hello-web:1.0 .` |
| `"/app.py": not found` | A file that the `COPY` line names is not in the folder where you ran the build. Go to the folder `hello-web`. |
| `repository name must be lowercase` | Use only lowercase letters in the name of the image. |
| `port is already allocated` | Port 8080 is in use. Run `docker rm -f hello`. Then use `-p 8081:8000` and open <http://localhost:8081>. |
| `The container name "/hello" is already in use` | Run `docker rm -f hello`. Then run the command again. |
| `executable file not found in $PATH` | The `CMD` line has a typing error. Correct it. Build again. Run `docker rm -f hello`. Run again. |
| No message, but the page does not load | Run `docker ps -a`. If the status is `Exited`, run `docker logs hello` to see the reason. If the `PORTS` column has no arrow, you forgot `-p 8080:8000`. |

## Clean your machine

Remove the containers first. Docker does not remove an image that a container uses.

```bash
docker rm -f hello
```

If you did the extra tasks, also remove their containers:

```bash
docker rm -f hello-2 hello-3
```

Then remove the image:

```bash
docker rmi hello-web:1.0
```

If you did extra task 3, also remove the second image:

```bash
docker rmi hello-web:2.0
```
