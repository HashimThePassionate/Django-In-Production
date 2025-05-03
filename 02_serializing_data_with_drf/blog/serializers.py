from rest_framework import serializers
from blog import models
from author.models import Author
from rest_framework import validators


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'


class BlogCustom2Serializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        print('*** Custom Update method ****')
        return super(BlogCustom2Serializer, self).update(instance, validated_data)

    class Meta:
        model = models.Blog
        fields = '__all__'


class BlogCustom3Serializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    tags = serializers.PrimaryKeyRelatedField(
        queryset=models.Tags.objects.all(), many=True, allow_empty=True
    )
    blog_cover_image = serializers.PrimaryKeyRelatedField(
        queryset=models.CoverImage.objects.all(),
    )

    class Meta:
        model = models.Blog
        fields = '__all__'


class BlogSerializer4(serializers.ModelSerializer):
    # Author ke name field tak pohanch
    author_name = serializers.CharField(source='author.name')

    class Meta:
        model = models.Blog
        fields = ['id', 'title', 'author_name']


class BlogLimitedFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = ['id', 'title', 'content', 'created_at']


class BlogExcludeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        exclude = ['updated_at']


class BlogReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'
        read_only_fields = ['updated_at']


class BlogExtraKwargsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'
        extra_kwargs = {
            'title': {'min_length': 10}
        }


class BlogDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'
        depth = 1


class CoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoverImage
        fields = ['image_link']


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tags
        fields = ['name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'email']


class BlogNestedSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    tags = TagsSerializer(many=True)
    cover_image = CoverImageSerializer(source='blog_cover_image')

    class Meta:
        model = models.Blog
        fields = ['id', 'title', 'content', 'author',
                  'tags', 'cover_image', 'created_at']


class BlogCustom3Serializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    tags = serializers.PrimaryKeyRelatedField(
        queryset=models.Tags.objects.all(), many=True, allow_empty=True
    )
    blog_cover_image = serializers.PrimaryKeyRelatedField(
        queryset=models.CoverImage.objects.all()
    )

    class Meta:
        model = models.Blog
        fields = '__all__'


# Serializer Method

class BlogCustom5Serializer(serializers.ModelSerializer):
    word_count = serializers.SerializerMethodField()

    def get_word_count(self, obj):
        return len(obj.content.split())  # Content ke words count karta hai

    class Meta:
        model = models.Blog
        fields = ['id', 'title', 'content', 'word_count']


# Serializer 2: Custom method name
class BlogCustom6CustomSerializer(serializers.ModelSerializer):
    word_count = serializers.SerializerMethodField(
        method_name='use_custom_word_count')

    def use_custom_word_count(self, obj):
        return len(obj.content.split())  # Same logic, different method name

    class Meta:
        model = models.Blog
        fields = ['id', 'title', 'content', 'word_count']
# Serializer 3: Related field example


class BlogRelatedSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    def get_author_name(self, obj):
        return obj.author.name.upper()  # Author ka naam uppercase mein

    class Meta:
        model = models.Blog
        fields = ['id', 'title', 'author_name']
