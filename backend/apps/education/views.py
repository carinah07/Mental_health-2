from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ContentNode
from .serializers import ContentNodeSerializer

@api_view(["GET"])
def list_root_nodes(request):
    node_type = request.query_params.get("type")
    if node_type not in ["user", "teacher", "parent"]:
        return Response({"error": "Invalid node type."}, status=status.HTTP_400_BAD_REQUEST)
    
    roots = ContentNode.objects.filter(parent=None, node_type=node_type)
    serializer = ContentNodeSerializer(roots, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def list_child_nodes(request, pk):
    try:
        parent = ContentNode.objects.get(pk=pk)
        children = parent.children.all()
        serializer = ContentNodeSerializer(children, many=True)
        return Response(serializer.data)
    except ContentNode.DoesNotExist:
        return Response({"error": "Parent node not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def get_node_details(request, pk):
    try:
        node = ContentNode.objects.get(pk=pk)
        serializer = ContentNodeSerializer(node)
        return Response(serializer.data)
    except ContentNode.DoesNotExist:
        return Response({"error": "Node not found."}, status=status.HTTP_404_NOT_FOUND)
