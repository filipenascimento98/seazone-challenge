from rest_framework import viewsets
from rest_framework.response import Response
from api.domain.anuncio import AnuncioDomain
from api.serializers.anuncio import (
    AnuncioOutputSerializer,
    AnuncioInputSerializer,
    AnuncioUpdateSerializer
)


class AnuncioView(viewsets.ViewSet):

    domain = AnuncioDomain()

    def create(self, request):
        serializer = AnuncioInputSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            ret = self.domain.criar(request.data)  
        
        if isinstance(ret, tuple):
            return Response({"message": ret[0] }, status=ret[1])
        
        return Response({"message": ret['message']}, status=ret['status'])
    
    def list(self, request):
        ret = self.domain.listar()

        if isinstance(ret, tuple):
            return Response({"message": ret[0] }, status=ret[1])

        serializer = AnuncioOutputSerializer(ret['message'], many=True)
        
        return Response(serializer.data, status=ret['status'])
    
    def retrieve(self, request, pk=None):
        ret = self.domain.obter(pk=pk)

        if isinstance(ret, tuple):
            return Response({"message": ret[0] }, status=ret[1])

        serializer = AnuncioOutputSerializer(ret['message'])
        
        return Response(serializer.data, status=ret['status'])
    
    def update(self, request, pk=None):
        serializer = AnuncioInputSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            ret = self.domain.atualizar(pk, request.data)  
        
        if isinstance(ret, tuple):
            return Response({"message": ret[0] }, status=ret[1])
        
        return Response({"message": ret['message']}, status=ret['status'])
    
    def partial_update(self, request, pk=None):
        serializer = AnuncioUpdateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            ret = self.domain.atualizar(pk, request.data)  
        
        if isinstance(ret, tuple):
            return Response({"message": ret[0] }, status=ret[1])
        
        return Response({"message": ret['message']}, status=ret['status'])