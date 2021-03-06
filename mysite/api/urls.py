from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^getMovieInfo/', views.getMovieInfo, name="movie"),
    url(r'^getMovieDetailInfo/', views.getMovieDetailInfo, name="moviedetail"),
    url(r'^getTheaterInfo/', views.getTheaterInfo, name="theater"),
    url(r'^getTheaterDetailInfo/', views.getTheaterDetailInfo, name="theaterdetail"),
    url(r'^getTheaterReserInfo/', views.getTheaterReserInfo, name="theaterreser"),
    url(r'^getMovieTimeReserInfo/', views.getMovieTimeReserInfo, name="movietimereserinfo"),
    url(r'^getSTReserInfo/', views.getSTReserInfo, name="getstReserInfo"),
    url(r'^getSeatInfo/', views.getSeatInfo, name="getSeatInfo"),
    url(r'^getUserDataDoLogin/', views.getUserDataDoLogin, name="getUserDataDoLogin"),
    url(r'^getNoticeInfo/', views.getNoticeInfo, name="getNoticeInfo"),
    url(r'^getNoticeDetailInfo/', views.getNoticeDetailInfo, name="getNoticeDetailInfo"),
    url(r'^getFreQueInfo/', views.getFreQueInfo, name="getFreQueInfo"),
    url(r'^getFreQueDetailInfo/', views.getFreQueDetailInfo, name="getFreQueDetailInfo"),
    url(r'^getScenarioInfo/', views.getScenarioInfo, name="getScenarioInfo"),
    url(r'^getScenarioDetailInfo/', views.getScenarioDetailInfo, name="getScenarioDetailInfo"),
    url(r'^getuser/', views.getuser, name="getuser"),
    url(r'^getMyFundingInfo/', views.getMyFundingInfo, name="getMyFundingInfo"),
    url(r'^getMyScenarioInfo/', views.getMyScenarioInfo, name="getMyScenarioInfo"),
    url(r'^fundingUpdate/(?P<pk>\d+)/$', views.FundingAccountView.as_view(), name="fundingUpdate"),
    url(r'^getOverlapJoin/', views.getOverlapJoin, name="getOverlapJoin"),
    url(r'^InsertWishiView/', views.InsertWishiView, name="InsertWishiView"),
    url(r'^getSTReserInfofo/', views.getSTReserInfofo, name="getSTReserInfofo"),
    url(r'^getUserDataDoLoginin/', views.getUserDataDoLoginin, name="getUserDataDoLoginin"),
    url(r'^getWishiView/', views.getWishiView, name="getWishiView"),
    url(r'^UpdateFundingView/', views.UpdateFundingView, name="UpdateFundingView"),
    url(r'^getWishiHeartView/', views.getWishiHeartView, name="getWishiHeartView"),
    url(r'^DeleteWishiView/', views.DeleteWishiView, name="DeleteWishiView"),
    url(r'^updateSeats/', views.updateSeats, name="updateSeats"),
    url(r'^IDSearchView/', views.IDSearchView, name="IDSearchView"),
    url(r'^PasswordSearchView/', views.PasswordSearchView, name="PasswordSearchView"),  
    url(r'^getreserlistView/', views.getreserlistView, name="getreserlistView"),
    url(r'^UserInfoupdateView/', views.UserInfoupdateView, name="UserInfoupdateView"),
    url(r'^UserpassupdateView/', views.UserpassupdateView, name="UserpassupdateView"),
    url(r'^getYetMovieInfo/', views.getYetMovieInfo, name="getYetMovieInfo"),
    url(r'^getPreMovieInfo/', views.getPreMovieInfo, name="getPreMovieInfo"),
    url(r'^InsertReviewView/', views.InsertReviewView, name="InsertReviewView"),
    url(r'^getReviewView/', views.getReviewView, name="getReviewView"),
    url(r'^CountScenarioInfo/', views.CountScenarioInfo, name="CountScenarioInfo"),
    url(r'^getreserdelistView/', views.getreserdelistView, name="getreserdelistView"),
    url(r'^UpdateReserDeView/', views.UpdateReserDeView, name="UpdateReserDeView"),
    url(r'^getScenarioNewsInfo/', views.getScenarioNewsInfo, name="getScenarioNewsInfo"),
    url(r'^getScenarioNewsDetailInfo/', views.getScenarioNewsDetailInfo, name="getScenarioNewsDetailInfo"),
    url(r'^getMyReviewView/', views.getMyReviewView, name="getMyReviewView"),
    url(r'^DeleteMyReviewView/', views.DeleteMyReviewView, name="DeleteMyReviewView"),
    url(r'^UpdateMyReviewView/', views.UpdateMyReviewView, name="UpdateMyReviewView"),
    url(r'^InsertAdminQView/', views.InsertAdminQView, name="InsertAdminQView"),
    url(r'^getAdminQView/', views.getAdminQView, name="getAdminQView"),
    url(r'^getJangRecommdation/', views.getJangRecommdation, name="getJangRecommdation"),
    url(r'^getResercurtimeView/', views.getResercurtimeView, name="getResercurtimeView"),
    url(r'^getNearLocation/', views.getNearLocation, name="getNearLocation"),
    url(r'^getNearLocationList/', views.getNearLocationList, name="getNearLocationList"),
   
    url(r'^getMtSeenMovieView/', views.getMtSeenMovieView, name="getMtSeenMovieView"),
    url(r'^getScenarioSearch/', views.getScenarioSearch, name="getScenarioSearch"),
    url(r'^getJangRecommdation2/', views.getJangRecommdation2, name="getJangRecommdation2"),
    url(r'^UpdateAmountView/', views.UpdateAmountView, name="UpdateAmountView"),
    url(r'^InsertMtSeenMovieView/', views.InsertMtSeenMovieView, name="InsertMtSeenMovieView"),
    url(r'^getmovieseenView/', views.getmovieseenView, name="getmovieseenView"),
    url(r'^getmovieseenList/', views.getmovieseenList, name="getmovieseenList"),
    url(r'^getJangRecommdation3/', views.getJangRecommdation3, name="getJangRecommdation3"),
    url(r'^getScenarioreward/', views.getScenarioreward, name="getScenarioreward"),

    url(r'^getSeats/', views.getSeats, name="getSeats"),
    url(r'^join/', views.Join.as_view()),
    url(r'^funding/', views.Funding.as_view())
]
