echo "Running pylint"
find src/opsgenie -name "*.py" -exec pylint -E {} \+
