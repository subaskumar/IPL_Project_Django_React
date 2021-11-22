from django.shortcuts import render
from rest_framework.views import APIView
from .models import Team,Player
from .serializers import TeamSerializer,PlayerSerializer
# TeamListSerializer
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse


class IPLTeam_API(APIView):      # Here APIView is subclasses of Django view clas
    def get(self, request, id = None, format = None):   # Here request id DRF's request instance, but not Django's HttpRequest instance
        if id is None:
            teams = Team.objects.all()
            serializer_team = TeamSerializer(teams,many=True, context= {'request': request})
            return Response(serializer_team.data)
        else :
            teams = Team.objects.get(id=id) 
            print(teams)
            serializer_team = TeamSerializer(teams,context= {'request': request})     
            return Response(serializer_team.data)
        
    def post(self,request, format = None):
        #print(request.body)        # You cannot access body after reading from request's data stream, it is already a stream data (DRF), in Django regular view we can access 'request.body'                
        print(type(request.data))   # <class 'dict'>
        serializer_data = TeamSerializer(data = request.data)
        if serializer_data.is_valid():
            serializer_data.save()       
            return Response({'msg': 'Data inserted sucessfully'})   
        return Response(serializer_data.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        
class Player_API(APIView):
    
    def get(self, request, id = None, format = None):
        if id is None:
            players = Player.objects.all()
            serializer_player = PlayerSerializer(players,many=True,context= {'request': request})
            return Response(serializer_player.data)
        else :
            player = Player.objects.get(id=id) 
            serializer_player = PlayerSerializer(player,context= {'request': request})     
            return Response(serializer_player.data)
               
# class IPLTeamList_API(APIView):  
#     def get(self, request, id = None, format = None):
#         if id is None:
#             teams = Team.objects.all()
#             serializer_team = TeamListSerializer(teams,many=True, context= {'request': request})
#             return Response(serializer_team.data)
#         else :
#             teams = Team.objects.get(id=id) 
#             serializer_team = TeamListSerializer(teams,context= {'request': request})     
#             return Response(serializer_team.data)
# from django.http import HttpResponseRedirect,JsonResponse,HttpResponse

@csrf_exempt
def Addplayer_view(request):
    if request.method=='POST':
        team = request.POST.get("team")
        team_query = Team.objects.get(teamName=team)
        playerName = request.POST.get("playerName")
        picture = request.FILES.get("picture")
        price = request.POST.get("price")
        isPlaying = request.POST.get("isPlaying")
        print(isPlaying)
        if isPlaying =="false":
            isPlaying = False
            print
        else:
            isPlaying = True   
        description = request.POST.get("description")
        
        res = Player(playerName = playerName, team = team_query, price = price, description =description,picture =picture,isPlaying = isPlaying )
        res.save()
        data = {
                    'message': 'successfully'
                }
        return JsonResponse(data,safe=False)