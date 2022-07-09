import graphene
from graphene_django import DjangoObjectType, DjangoListField
from Account.models import ModelUsers, CustomUser
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

# class Query(UserQuery, MeQuery, graphene.ObjectType):
#     pass

# class AuthMutation(graphene.ObjectType):
#     register = mutations.Register.Field()
#     verify_account = mutations.VerifyAccount.Field()
#     token_auth = mutations.ObtainJSONWebToken.Field()
#     update_account = mutations.UpdateAccount.Field()

# class Mutation(AuthMutation, graphene.ObjectType):
#     pass


class ModelUsersType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email','isActive','created_on','updated_on')

class CreateModelUsersType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')



class Query(graphene.ObjectType):
    users = graphene.Field(ModelUsersType, id=graphene.Int())
    
    def resolve_users(root, info, id):
        try:
            return CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return None
    
            
class ModelUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        
    user = graphene.Field(CreateModelUsersType)
    
    @classmethod
    def mutate(cls, root, info, username, email, password):
        try:
            check = CustomUser.objects.get(email=email)
            if check is not None:
                raise Exception('Email already exists')
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(username=username, email=email, password=password)
            user.isActive = True
            user.save()
            return ModelUserMutation(user=user)
   
        
class Mutation(graphene.ObjectType):
    create_user = ModelUserMutation.Field()   
   


schema = graphene.Schema(query=Query, mutation=Mutation)