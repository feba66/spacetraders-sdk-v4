import_statement = "from burstylimiter import BurstyLimiter, Limiter"
target_function = "    def call_api("
function_decorator = "    @BurstyLimiter(Limiter(2, 1), Limiter(30, 60))"

target_file = "tmp/generated/openapi_client/api_client.py"

with open(target_file, "r") as file:
    lines = file.readlines()

added_import = False
with open(target_file, "w") as file:
    for line in lines:
        if target_function in line:
            file.write(function_decorator + "\n")
        if line.startswith("import") and not added_import:
            file.write(import_statement + "\n")
            added_import = True
        file.write(line)
