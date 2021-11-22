from rest_framework import serializers
from django.db.models import Q
from .models import Team,Player
        
# class PlayerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Player
#         fields = "__all__"     
#     def to_representation(self, instance):          # here we override this method and instance is player class instance
#         rep = super().to_representation(instance)   # it returns data of Player instance
#         T_name = TeamSerializer(instance.team).data
#         rep["team"]=T_name["teamName"]
#         return rep

#######################################

class PlayerSerializer(serializers.ModelSerializer):
    team = serializers.StringRelatedField()         # StringRelatedField may be used to represent the target 
                                                    # of the relationship using its __str__ method.
    class Meta:
        model = Player
        fields = "__all__"
        
class TeamSerializer(serializers.ModelSerializer):
    total_player = serializers.SerializerMethodField()
    Batsman = serializers.SerializerMethodField()
    Bowler = serializers.SerializerMethodField()
    icon = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Team
        fields = ['id','teamName','champ_win','icon','total_player','Batsman','Bowler']
    
    def get_total_player(self, obj):
        players = Player.objects.filter(team__teamName=obj.teamName).count()
        return players
    
    def get_Batsman(self,obj):
        batsmans = Player.objects.filter(Q(team__teamName=obj.teamName) & Q(description = "batsman"))
        request = self.context.get("request")
        serializer_batsman = PlayerSerializer(batsmans, many =True,context= {'request': request})
        return serializer_batsman.data
    
    
    def get_Bowler(self,obj):
        bowlers = Player.objects.filter(Q(team__teamName=obj.teamName) & Q(description = "bowler"))
        request = self.context.get("request")
        serializer_bowler = PlayerSerializer(bowlers, many =True,context= {'request': request})
        return serializer_bowler.data
        
# class TeamListSerializer(serializers.ModelSerializer):
#     total_player = serializers.SerializerMethodField()
#     class Meta:
#         model = Team
#         fields = "__all__"
        
#     def get_total_player(self, obj):
#         players = Player.objects.filter(team__teamName=obj.teamName).count()
#         return players
    