kubectl create namespace sheep
kubectl apply -f k8s/frontend.yaml -n sheep
kubectl apply -f k8s/backend.yaml -n sheep
kubectl apply -f k8s/generator.yaml -n sheep
kubectl apply -f k8s/collector.yaml -n sheep
kubectl apply -f k8s/secret.yaml -n sheep
kubectl create namespace dynatrace
kubectl apply -f https://github.com/Dynatrace/dynatrace-operator/releases/download/v0.13.0/kubernetes.yaml
kubectl -n dynatrace wait pod --for=condition=ready --selector=app.kubernetes.io/name=dynatrace-operator,app.kubernetes.io/component=webhook --timeout=300s
kubectl apply -f k8s/dt-secret.yaml -n dynatrace
kubectl apply -f k8s/activegate.yaml -n dynatrace
