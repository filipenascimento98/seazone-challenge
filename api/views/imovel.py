from rest_framework.response import Response
from rest_framework import viewsets
from api.domain.imovel import ImovelDomain
from api.serializers.imovel import (
    ImovelOutputSerializer,
    ImovelInputSerializer,
)

class ImovelView(viewsets.ViewSet):

    domain = ImovelDomain()

    def list(self, request):
        ret = self.domain.listar()

        if isinstance(ret, tuple):
            return Response({"message": ret[0]}, status=ret[1])

        serializer = ImovelOutputSerializer(ret['message'], many=True)
        
        return Response(serializer.data, status=ret['status'])

    def retrieve(self, request, pk=None):
        ret = self.domain.obter(pk=pk)
        
        if isinstance(ret, tuple):
            return Response({"message": ret[0]}, status=ret[1])

        serializer = ImovelOutputSerializer(ret['message'])

        return Response(serializer.data, status=ret['status'])

    def create(self, request):
        serializer = ImovelInputSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            ret = self.domain.criar(serializer.data)
        
        if isinstance(ret, tuple):
            return Response({"message": ret[0]}, status=ret[1])
        
        return Response({"message": ret['message']}, status=ret['status'])

    def update(self, request, pk=None):
        serializer = ImovelInputSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            ret = self.domain.atualizar(pk, serializer.data)
        
        if isinstance(ret, tuple):
            return Response({"message": ret[0]}, status=ret[1])
        
        return Response({"message": ret['message']}, status=ret['status'])

    def partial_update(self, request, pk=None):
        ret = self.domain.atualizar(pk, request.data)

        if isinstance(ret, tuple):
            return Response({"message": ret[0]}, status=ret[1])

        return Response({"message": ret['message']}, status=ret['status'])

    def destroy(self, request, pk=None):
        ret = self.domain.excluir(pk=pk)

        if isinstance(ret, tuple):
            return Response({"message": ret[0]}, status=ret[1])
        
        return Response(status=ret['status'])