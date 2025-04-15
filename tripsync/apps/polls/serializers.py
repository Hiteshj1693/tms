# from rest_framework import serializers
# from apps.polls.models import Poll, PollOption, Vote

# class PollOptionSerializer(serializers.ModelSerializer):
#     votes_count = serializers.IntegerField(source = 'votes.count', read_only=True)

#     class Meta:
#         model = PollOption
#         fields = ['id','poll','text','votes_count']
    
# class PollSerializer(serializers.ModelSerializer):
#     options = PollOptionSerializer(many = True, read_only = True)
#     total_votes = serializers.SerializerMethodField()

#     class Meta:
#         model = Poll
#         fields = ['id','trip','question','created_by','created_at','expires_at','is_active','option','total_votes']

#     def get_total_votes(self,obj):
#         return Vote.objects.filter(option__poll=obj).count()
#     def create(self, validated_data):
#         options_data = validated_data.pop('options')
#         poll = Poll.objects.create(**validated_data)
#         for option in options_data:
#             PollOption.objects.create(poll=poll, **option)
#         return poll
    

# class VoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vote
#         fields = ['id','user','option','voted_at']


from rest_framework import serializers
from .models import Poll, PollOption, Vote
from apps.users.models import User  # Assuming you're using a custom User model
from apps.trips.models import Trip


class PollOptionSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = PollOption
        fields = ['id', 'text', 'votes_count']


class PollCreateSerializer(serializers.ModelSerializer):
    options = serializers.ListField(
        child=serializers.CharField(max_length=255),
        write_only=True
    )

    class Meta:
        model = Poll
        fields = ['id', 'trip', 'question', 'created_by', 'options']

    def create(self, validated_data):
        options = validated_data.pop('options')
        poll = Poll.objects.create(**validated_data)
        for option_text in options:
            PollOption.objects.create(poll=poll, text=option_text)
        return poll
    
class VoteSerializer(serializers.ModelSerializer):
    voted_by = serializers.StringRelatedField()
    option_text = serializers.CharField(source='option.text', read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'poll', 'option', 'option_text', 'voted_by', 'voted_at']


class PollDetailSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True, read_only=True)
    total_votes = serializers.SerializerMethodField()
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'trip', 'question', 'created_by', 'is_active', 'created_at', 'options', 'votes','total_votes']

    def get_total_votes(self, obj):
        return obj.votes.count()


class VoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['poll', 'option', 'voted_by']

    def validate(self, data):
        poll = data.get('poll')
        voted_by = data.get('voted_by')

        if not poll.is_active:
            raise serializers.ValidationError("This poll is not active.")

        if Vote.objects.filter(poll=poll, voted_by=voted_by).exists():
            raise serializers.ValidationError("User has already voted in this poll. Use update if changing vote.")

        return data

    def create(self, validated_data):
        return Vote.objects.create(**validated_data)


class VoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['option']

    def update(self, instance, validated_data):
        instance.option = validated_data.get('option', instance.option)
        instance.save()
        return instance


# class VoteSerializer(serializers.ModelSerializer):
#     poll = serializers.StringRelatedField()
#     option = serializers.StringRelatedField()
#     voted_by = serializers.StringRelatedField()

#     class Meta:
#         model = Vote
#         fields = ['id', 'poll', 'option', 'voted_by', 'voted_at']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['poll', 'option']  # remove 'voted_by'

    # def create(self, validated_data):
    #     user = self.context['request'].user  # get the user from the request
    #     validated_data['voted_by'] = user
    #     return super().create(validated_data)

    def create(self, validated_data):
        user = self.context['request'].user
        poll = validated_data['poll']
        option = validated_data['option']

        # Check for existing vote
        try:
            vote = Vote.objects.get(poll=poll, voted_by=user)
            # Decrease count of previous option
            vote.option.votes_count = F('votes_count') - 1
            vote.option.save(update_fields=["votes_count"])

            vote.option = option
            vote.voted_at = timezone.now()
            vote.save()

        except Vote.DoesNotExist:
            vote = Vote.objects.create(poll=poll, option=option, voted_by=user)

        # Increase count of new option
        option.votes_count = F('votes_count') + 1
        option.save(update_fields=["votes_count"])

        return vote


