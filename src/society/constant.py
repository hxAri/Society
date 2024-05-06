#!/usr/bin/env python3

#
# @author Ari Setiawan
# @create 12.01-2024 14:31
# @github https://github.com/hxAri/Society
#
# Society Copyright (c) 2024 - Ari Setiawan <hxari@proton.me>
# Society Licence under GNU General Public Licence v3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# Society Program is not affiliated with or endorsed, endorsed at all by
# Facebook or any other party, if you use the main account to use this
# tool we as Coders and Developers are not responsible for anything that
# happens to that account, use it at your own risk, and this is Strictly
# not for SPAM.
#

from society.common import strftime, timestamp
from society.filter import Filter
from society.typing.schema import Schema
from society.search import Search


# Constant of Facebook API Request Friendly

# CommentListComponentsRootQuery|7499082470113234 variables {"commentsIntentToken":"RANKED_UNFILTERED_CHRONOLOGICAL_REPLIES_INTENT_V1","feedLocation":"DEDICATED_COMMENTING_SURFACE","feedbackSource":110,"focusCommentID":null,"scale":1,"useDefaultActor":false,"id":"ZmVlZGJhY2s6Nzc2MTcwODkxMjA4NTU2"}

SCHEMA_COMMENT_LIST:Schema = Schema( "CometUFICommentsProviderForDisplayCommentsQuery", 5315135448570862 )
# SCHEMA_COMMENT_LIST:Schema = Schema( "CommentListComponentsRootQuery", 7109884639093867 )
""" Facebook Graphql Schema for get comment list from feedback """

SCHEMA_COMMENT_LIST_DEPTH:Schema = Schema( "Depth{}CommentsListPaginationQuery", 0 )
""" Facebook Graphql Schema for get comment list by depth level comment """

SCHEMA_COMMENT_TOOL_TIP:Schema = Schema( "CometUFICommentsCountTooltipContentQuery", 6744097142294862 )
""" Facebook Graphql Schema for get comment list tool tip from feedback """

SCHEMA_FEED:Schema = Schema( "CometSinglePostContentQuery", 0 )
""" Facebook Graphql Schema for get feedback info """

SCHEMA_FEED_GROUP:Schema = Schema( "GroupsCometFeedRegularStoriesPaginationQuery", 24605537559061066 )
""" Facebook Graphql Schema for get feedback timeline of group """

SCHEMA_FEED_NEWS:Schema = Schema( "CometNewsFeedPaginationQuery", 0 )
""" Facebook Graphql Schema for get feedback timeline of news """

SCHEMA_FEED_PAGE:Schema = Schema( "CometModernPageFeedPaginationQuery", 7029869947082163 )
""" Facebook Graphql Schema for get feedback timeline of page """

SCHEMA_FEED_PROFILE:Schema = Schema( "ProfileCometTimelineFeedRefetchQuery", 6883950815060109 )
""" Facebook Graphql Schema for get feedback timeline of user """

SCHEMA_FEED_PROFILE_MENTION:Schema = Schema( "ProfileCometMentionsFeedRefetchQuery", 0 )
""" Facebook Graphql Schema for get feedback timeline mention of user """

SCHEMA_FEED_RESHARE:Schema = Schema( "CometResharesFeedPaginationQuery", 7009845242445262 )
""" Facebook Graphql Schema for get feedback reshared """

SCHEMA_LIKE_COUNT:Schema = Schema( "FBReelsFeedbackLikeQuery", 0 )
""" Facebook Graphql Schema for get feedback like count """

SCHEMA_LIKE_LIST:Schema = Schema( "CometUFIReactionsDialogQuery", 0 )
""" Facebook Graphql Schema for get feedback like list user """

SCHEMA_LIKE_TOOL_TIP:Schema = Schema( "CometUFIReactionIconTooltipContentQuery", 6235145276554312 )
""" Facebook Graphql Schema for get feedback like list tool tip """
# {"feedbackTargetID":"ZmVlZGJhY2s6ODEzNTIzNTYzNDczMzYz","reactionID":"1678524932434102"}

SCHEMA_PHOTO:Schema = Schema( "CometPhotoRootContentQuery", 6872357066208103 )
""" Facebook Graphql Schema for get photo """
# {"isMediaset":true,"renderLocation":"permalink","nodeID":"812878573537862","mediasetToken":"pb.100044471797939.-2207520000","scale":1,"feedLocation":"COMET_MEDIA_VIEWER","feedbackSource":65,"focusCommentID":null,"glbFileURIHackToRenderAs3D_DO_NOT_USE":null,"privacySelectorRenderLocation":"COMET_MEDIA_VIEWER","useDefaultActor":false,"useHScroll":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}

SCHEMA_PROFILE:Schema = Schema( "ProfileCometHeaderQuery", 7076249805805101 )
""" Facebook Graphql Schema for get profile info """
# {"scale":1,"selectedID":"100044466906442","selectedSpaceType":"community","shouldUseFXIMProfilePicEditor":false,"userID":"100044466906442"}

SCHEMA_PROFILE_ABOUT:Schema = Schema( "ProfileCometAboutAppSectionQuery", 7456271131096329 )
""" Facebook Graphql Schema for get profile info (About) """
# {"appSectionFeedKey":"ProfileCometAppSectionFeed_timeline_nav_app_sections__100064469571787:2327158227","collectionToken":null,"pageID":"100064469571787","rawSectionToken":"100064469571787:2327158227","scale":1,"sectionToken":"YXBwX3NlY3Rpb246MTAwMDY0NDY5NTcxNzg3OjIzMjcxNTgyMjc=","showReactions":true,"userID":"100064469571787","__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}

SCHEMA_PROFILE_FOLLOWER:Schema = Schema( "ProfileCometTopAppSectionQuery", 7301866803205703 )
""" Facebook Graphql Schema for get profile info (Follower) """
# {"collectionToken":"YXBwX2NvbGxlY3Rpb246MTAwMDQ0NDcxNzk3OTM5OjIzNTYzMTgzNDk6MzI=","feedbackSource":65,"feedLocation":"COMET_MEDIA_VIEWER","scale":1,"sectionToken":"YXBwX3NlY3Rpb246MTAwMDQ0NDcxNzk3OTM5OjIzNTYzMTgzNDk=","userID":"100044471797939","__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}

SCHEMA_PROFILE_FOLLOWER_SCROLL:Schema = Schema( "ProfileCometAppCollectionListRendererPaginationQuery", 24973057805674571 )
""" Facebook Graphql Schema for get profile info (Follower-scroll) """
# {"count":8,"cursor":"AQHRY1Ei1kfpl92hflQYJND4AIFzQPAW9bpw115AI777ebnQHyfu7Fx601_AXYZsP9lYCCAYAuKha03nZhAvEziwpQ","scale":1,"search":"{user}","id":"app_collection:{user-id}:2356318349:32"}

SCHEMA_PROFILE_LOGEDOT:Schema = Schema( "CometHovercardQueryRendererQuery", 0 )
""" Facebook Graphql Schema for get profile info (Logedot) """
# {"actionBarRenderLocation":"WWW_COMET_HOVERCARD","context":"DEFAULT","entityID":"100089826347949","includeTdaInfo":false,"scale":1}

SCHEMA_PROFILE_LOGGED_OUT:Schema = Schema( "ProfilePlusCometLoggedOutRootQuery", 7467132690047501 )
""" Facebook Graphql Schema for get profile info (LoggedOut) """
# {"scale":1,"userID":"100044466906442"}

SCHEMA_PROFILE_MENTION:Schema = Schema( "ProfileCometMentionsFeedQuery", 0 )
""" Facebook Graphql Schema for get profile info (Mention) """

SCHEMA_PROFILE_PHOTO:Schema = Schema( "ProfileCometTopAppSectionQuery", 7301866803205703 )
""" Facebook Graphql Schema for get profile info (Photo) """
# {"collectionToken":null,"feedbackSource":65,"feedLocation":"COMET_MEDIA_VIEWER","scale":1,"sectionToken":"YXBwX3NlY3Rpb246MTAwMDQ0NDcxNzk3OTM5OjIzMDUyNzI3MzI=","userID":"100044471797939","__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}

SCHEMA_PROFILE_PHOTO_CURSOR:Schema = Schema( "ProfileCometAppCollectionPhotosRendererPaginationQuery", 6684543058255697 )
""" Facebook Graphql Schema for get profile info (Photo-Cursor) """
# {"count":8,"cursor":"AQHRUISzpX3Pmtkg9c-2RE58v3un8Gp3_82MUljrlrPjz1esyb6i64VxUThm0usHzoDG6KAA1YE-9GgwL5owAW_Gsg","scale":1,"id":"YXBwX2NvbGxlY3Rpb246MTAwMDQ0NDcxNzk3OTM5OjIzMDUyNzI3MzI6NA=="}

SCHEMA_PROFILE_REELS:Schema = Schema( "ProfileCometTopAppSectionQuery", 7301866803205703 )
""" Facebook Graphql Schema for get profile info (Reels) """
# {"collectionToken":null,"feedbackSource":65,"feedLocation":"COMET_MEDIA_VIEWER","scale":1,"sectionToken":"YXBwX3NlY3Rpb246MTAwMDQ0NDcxNzk3OTM5OjE2ODY4NDg0MTc2ODM3NQ==","userID":"100044471797939","__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}

SCHEMA_PROFILE_REELS:Schema = Schema( "ProfileCometAppCollectionReelsRendererPaginationQuery", 6893781087396893 )
""" Facebook Graphql Schema for get profile info (Reels-Cursor) """
# {"count":10,"cursor":"AQHRabPTxI4MV70Bq66TKNM76kxEwOyQsviQYI3ZUXCEzG3P1njetUvS9F2MuZbWSpOQhAyfa4tKkxCBPVlUzCMtcg","feedLocation":"COMET_MEDIA_VIEWER","feedbackSource":65,"focusCommentID":null,"renderLocation":null,"scale":1,"useDefaultActor":true,"id":"YXBwX2NvbGxlY3Rpb246MTAwMDY0NDY5NTcxNzg3OjE2ODY4NDg0MTc2ODM3NToyNjA="}

SCHEMA_PROFILE_VIDEO:Schema = Schema( "CometProfilePlusVideosRootQuery", 7290661444354304 )
""" Facebook Graphql Schema for get profile info (Video) """
# {"feedbackSource":86,"feedLocation":"PROFILE_PLUS_TIMELINE","focusCommentID":null,"pageID":"1420915858167871","scale":4,"shouldLoadAdminControls":false,"showReactions":true,"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}

SCHEMA_PROFILE_VIDEO_CURSOR:Schema = Schema( "PagesCometChannelTabAllVideosCardImplPaginationQuery", 24979495425027781 )
""" Facebook Graphql Schema for get profile info (Video-Cursor) """
# {"alwaysIncludeAudioRooms":true,"count":6,"cursor":"AQHRf0dolVk8lq389wHBB_U7_ALzgvCXAJN5pJljB4BXn7NolLs-t2Fi2CmoXFm-Huc8pFpivUa-biVNNhu__EH4GQ","pageID":"1420915858167871","scale":4,"showReactions":true,"useDefaultActor":false,"id":"1420915858167871"}

SCHEMA_REEL:Schema = Schema( "FBReelsRootWithEntrypointQuery", 0 )
""" Facebook Graphql Schema for get reel info """

SCHEMA_SEARCH:Schema = Schema( "SearchCometResultsInitialResultsQuery", 0 )
""" Facebook Graphql Schema for search by keyword """

SCHEMA_SEARCH_lOCATION_HINT:Schema = Schema( "useSearchCometFilterTypeaheadTypedDataSourceQuery", 0 )
""" Facebook Graphql Schema for search loaction hint """


# Constant of Facebook Search Filter

FILTER_GROUP_LOCATION:Filter = Filter( "filter_groups_location", None )
""" Constant Facebook Search Filter based on Location ID """

FILTER_GROUP_PUBLIC:Filter = Filter( "public_groups", None )
""" Constant Facebook Search Filter based on Public Group """

FILTER_PAGE_CATEGORY:Filter = Filter( "pages_category", None )
""" Constant Facebook Search Filter based on Page Category """

FILTER_POST_CREATION:Filter = Filter( "creation_time", {
	"start_year": strftime( "%Y", timestamp() ),
	"start_month": strftime( "%Y-%m", timestamp() ),
	"end_year": strftime( "%Y", timestamp() ),
	"end_month": strftime( "%Y-12", timestamp( months=0x1 ) ),
	"start_day": strftime( "%Y-%m-%d", timestamp( days=0x1 ) ),
	"end_day": strftime( "%Y-12-31", timestamp() ),
})
""" Constant Facebook Search Filter based on Post Creation """

FILTER_POST_RECENT:Filter = Filter( "recent_posts", None )
""" Constant Facebook Search Filter based on POSt Recent """
 

# Constant of Facebook Search TAB

SEARCH_GROUP:Search = Search( "GROUPS_TAB", filters=[ FILTER_GROUP_PUBLIC, FILTER_GROUP_LOCATION ] )
""" Facebook Search TAB Group """

SEARCH_PAGE:Search = Search( "PAGES_TAB", filters=[ FILTER_PAGE_CATEGORY ] )
""" Facebook Search TAB Page """

SEARCH_POST:Search = Search( "POSTS_TAB", filters=[ FILTER_POST_RECENT, FILTER_POST_CREATION ] )
""" Facebook Search TAB Post """
