from rest_framework import viewsets
from rest_framework.response import Response
from api.domain.reserva import ReservaDomain
from api.serializers.reserva import (
    ReservaOutputSerializer,
    ReservaInputSerializer
)


class ReservaView(viewsets.ViewSet):
    domain = ReservaDomain()

    def list(self, request):
        ret = self.domain.listar()

        if isinstance(ret, tuple):
            return Response({"message": ret[0]}, status=ret[1])

        serializer = ReservaOutputSerializer(data=ret['message'], many=True)

        return Response(serializer.data, status=ret['status'])
    
    def retrieve(self, request, pk=None):
        ret = self.domain.obter(pk=pk)

        if isinstance(ret, tuple):
            return Response({"message": ret[0]}, status=ret[1])
        
        serializer = ReservaOutputSerializer(data=ret['message'])

        return Response(serializer.data, status=ret['status'])
    
    def create(self, request):
        serializer = ReservaInputSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            ret = self.domain.criar(serializer.data)
        
        if isinstance(ret, tuple):
            return Response({"message": ret[0]}, status=ret[1])

        return Response(serializer.data, status=ret['status']) 
    
    def destroy(self, request, pk=None):
        ret = self.domain.excluir(pk=pk)

        if isinstance(ret, tuple):
            return Response({"message": ret[0]}, status=ret[1])
        
        return Response(status=ret['status'])
        
