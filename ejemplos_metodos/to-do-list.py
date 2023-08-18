from fastapi import FastAPI, HTTPException

app = FastAPI()

# Lista para almacenar tareas
tasks = []

# Ruta para crear una tarea
@app.post("/tasks/", response_model=dict)
def create_task(task: dict):
    tasks.append(task)
    return task

# Ruta para obtener todas las tareas
@app.get("/tasks/", response_model=list)
def get_tasks():
    return tasks

# Ruta para obtener una tarea por su ID
@app.get("/tasks/{task_id}", response_model=dict)
def get_task(task_id: int):
    if task_id < len(tasks):
        return tasks[task_id]
    raise HTTPException(status_code=404, detail="Task not found")
