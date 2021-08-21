::for /f  "tokens=1 delims= " %%i in (install.log) do echo %%i
@for /f  "tokens=1 delims= " %%i in (install.log) do del %%i
rmdir /q /s build
rmdir /q /s dist
rmdir /q /s iprs.egg-info
@echo =======================================
@echo     IPRS has been uninstalled!
@echo =======================================
pause