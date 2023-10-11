kubectl create namespace sheep
kubectl apply -f k8s/frontend.yaml -n sheep
kubectl apply -f k8s/backend.yaml -n sheep
kubectl apply -f k8s/generator.yaml -n sheep
kubectl apply -f k8s/collector.yaml -n sheep
kubectl apply -f k8s/secret.yaml -n sheep
