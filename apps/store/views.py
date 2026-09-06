from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import FeatureFlag, SocialLink, StoreLocation, StoreSettings
from .serializers import SocialLinkSerializer, StoreLocationSerializer, StoreSettingsSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def storefront_config(request):
    store = StoreSettings.objects.order_by("created_at").first() or StoreSettings()
    social_links = SocialLink.objects.filter(is_active=True).order_by("sort_order", "key")
    locations = StoreLocation.objects.filter(is_active=True).order_by("sort_order", "name")

    return Response(
        {
            "store": StoreSettingsSerializer(store).data,
            "social_links": SocialLinkSerializer(social_links, many=True).data,
            "locations": StoreLocationSerializer(locations, many=True).data,
            "features": FeatureFlag.resolved(),
        }
    )
