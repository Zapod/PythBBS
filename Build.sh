echo "Building Directories"
echo "Menus..."
mkdir "./Menus"
mkdir "./MenuCONFIG"



echo " 				 PythBBS Main Menu " > ./Menus/Main.mnu
echo "" >> ./Menus/Main.mnu
echo "		A) System Bullitens		B) Message Menu " >> ./Menus/Main.mnu
echo "		Q) Quit						" >> ./Menus/Main.mnu

echo "				    Message Menu " > ./Menus/Message.mnu
echo ""
echo "		      P) Post Message 	        V) View Posts " >> ./Menus/Message.mnu
echo " 		      S) Select Base " >> ./Menus/Message.mnu


echo " 			Good Bye User! " > ./Menus/GoodByeSplash.mnu
echo " " >> ./Menus/GoodByeSplash.mnu
echo " " >> ./Menus/GoodByeSplash.mnu
echo "	Have a good day and return back to <BBSNAME> Soon! " >> ./Menus/GoodByeSplash.mnu



echo " A) General " > ./Menus/BASE.mnu
echo " B) Tech " >> ./Menus/BASE.mnu
echo " C) Back" >> ./Menus/BASE.mnu

echo " # Config file for Main Menu" > ./MenuCONFIG/Main.config
echo " Main | 2 " >> ./MenuCONFIG/Main.config
echo " A = LINKTO DEFAULT" >> ./MenuCONFIG/Main.config
echo " B = GOTO Message" >> ./MenuCONFIG/Main.config

echo " # Config file for Message Menu" >  ./MenuCONFIG/Message.config
echo " Message | 3 " >> ./MenuCONFIG/Message.config
echo " P = POST" >> ./MenuCONFIG/Message.config
echo " V =  VIEW" >> ./MenuCONFIG/Message.config
echo " S = GOTO BASE" >> ./MenuCONFIG/Message.config

echo " # Config File for Base Select " > ./MenuCONFIG/BASE.config
echo " BASE | 3 " >> ./MenuCONFIG/BASE.config
echo " A = SELECT General" >> ./MenuCONFIG/BASE.config
echo " B = SELECT Tech " >> ./MenuCONFIG/BASE.config
echo " C = GOTO Message" >> ./MenuCONFIG/BASE.config

mkdir ./TextFiles/
echo " 			Welcome To PythBBS!" > ./TextFiles/DEFAULT.txt
echo " " >> ./TextFiles/DEFAULT.txt
echo " BBS software, written in Python, easily customizable!" >> ./TextFiles/DEFAULT.txt
echo " https://github.com/Zapod/PythBBS/ - Project github" >> ./TextFiles/Default.txt


echo "./Posts... "
mkdir "./Posts"
mkdir "./Posts/General"
mkdir "./Posts/Tech/"
echo " " > "./Posts/General/MessageTree.dat"
echo " " > "./Posts/Tech/MessageTree.dat"
