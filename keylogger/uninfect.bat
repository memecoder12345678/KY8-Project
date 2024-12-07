::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFDpQQQ2MAE+/Fb4I5/jHxumIrGoPW/cvKcHS2bvu
::YAwzuBVtJxjWCl3EqQJhSA==
::ZR4luwNxJguZRRmw3A8TJx9RLA==
::Yhs/ulQjdFy5
::cxAkpRVqdFKZSzk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSTk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+IeA==
::cxY6rQJ7JhzQF1fEqQJhZksaHGQ=
::ZQ05rAF9IBncCkqN+0xwdVsFAlTMbAs=
::ZQ05rAF9IAHYFVzEqQIbEUM0
::eg0/rx1wNQPfEVWB+kM9LVsJDC+7ZAs=
::fBEirQZwNQPfEVWB+kM9LVsJDC+7ZAs=
::cRolqwZ3JBvQF1fEqQIlJhJaSgGBKAs=
::dhA7uBVwLU+EWG2suWE/LB40
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATE100gMQldSwyWfMlzRudMury3r96v704SUOdf
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFDpQQQ2MAE+/Fb4I5/jHxNPf7EgFUYI=
::YB416Ek+ZW8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v AVAADA /f
attrib -s -h -r %userprofile%\Desktop\keylogger.exe
taskkill /f /im keylogger.exe
del %userprofile%\Desktop\keylogger.exe
