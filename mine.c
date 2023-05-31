#include<stdlib.h>
#include<time.h>

#include<raylib.h>
#include<raymath.h>


#define Rows 10
#define Cols 10


const int screenheight=400;
const int screenwidth=400;

float starttime;
float endtime;

const int blockheight=screenheight/Rows;
const int blockwidth=screenwidth/Cols;
const char* youlose="YOU LOSE!";
const char* restart="Press 'r' to Play Again";
const char* youwin="YOU WIN";

int blocksrevealed;
int minespresent;
typedef struct Block{
    int i;  
    int j;
    bool containsmine; 
    bool revealed;
    int MinesAround;
    bool flagged;
    bool tile;
} Block;
typedef enum GameState{
    PLAYING,
    LOSE,
    WIN
}GameState;
GameState state=PLAYING;
Block grid[Cols][Rows];
Texture2D flagSprite;
Texture2D mineSprite;
Texture2D tileSprite;
Texture2D emoji;
Texture2D happyemoji;
Sound sound;
Sound sound2;

void DrawBlock(Block printB){ 
    if(printB.tile && !printB.flagged){
        Rectangle source={0,0,tileSprite.width,tileSprite.height};
        Rectangle dest = {printB.i*blockwidth+4,printB.j*blockheight+4,blockwidth-6,blockheight-6};
        Vector2 origin={0,0};

        DrawTexturePro(tileSprite,source,dest,origin, 0.0f,WHITE);
    }
    else if(printB.revealed){
        if(printB.containsmine){
            DrawRectangle(printB.i*blockwidth,printB.j*blockheight,blockwidth,blockheight,RED);
			Rectangle source={0,0,mineSprite.width,mineSprite.height};
            Rectangle dest = {printB.i*blockwidth+3,printB.j*blockheight+3,blockwidth-8,blockheight-8};
            Vector2 origin={0,0};

            DrawTexturePro(mineSprite,source,dest,origin, 0.0f,WHITE); 
        }else{
            DrawRectangle(printB.i*blockwidth,printB.j*blockheight,blockwidth,blockheight,LIGHTGRAY);
            if(printB.MinesAround ==1){
            DrawText(TextFormat("%d",printB.MinesAround),printB.i*blockwidth+12,printB.j*blockheight+6,blockheight-8,BLUE);
            }
            if(printB.MinesAround ==2){
            DrawText(TextFormat("%d",printB.MinesAround),printB.i*blockwidth+12,printB.j*blockheight+6,blockheight-8,PINK);
            }
            if(printB.MinesAround ==3){
            DrawText(TextFormat("%d",printB.MinesAround),printB.i*blockwidth+12,printB.j*blockheight+6,blockheight-8,RED);
            }
            if(printB.MinesAround ==4){
            DrawText(TextFormat("%d",printB.MinesAround),printB.i*blockwidth+12,printB.j*blockheight+6,blockheight-8,YELLOW);
            }
            if(printB.MinesAround ==5){
            DrawText(TextFormat("%d",printB.MinesAround),printB.i*blockwidth+12,printB.j*blockheight+6,blockheight-8,MAROON);
            }
            if(printB.MinesAround >5){
            DrawText(TextFormat("%d",printB.MinesAround),printB.i*blockwidth+12,printB.j*blockheight+6,blockheight-8,DARKGRAY);
            }
        }
    }else if(printB.flagged){
        Rectangle source={0,0,flagSprite.width,flagSprite.height};
        Rectangle dest = {printB.i*blockwidth+4,printB.j*blockheight+4,blockwidth-6,blockheight-6};
        Vector2 origin={0,0};

        DrawTexturePro(flagSprite,source,dest,origin, 0.0f,WHITE);
    }
    DrawRectangleLines(printB.i*blockwidth,printB.j*blockheight,blockwidth,blockheight,BLACK);
}
bool IsValidIndex(int i,int j){
    return i>=0 && i<Cols &&j>=0 && j<Rows;
}
void Clear(){
	for(int i=0;i<Cols;i++){
        for(int j=0;j<Rows;j++){
			if(grid[i][j].revealed==false){
				grid[i][j].revealed=true;
                grid[i][j].tile=false;

			}
		}
	}
	
}

void BlockReveal(int i,int j){
    if(grid[i][j].flagged){
        return;
    }
    grid[i][j].revealed=true;
    grid[i][j].tile=false;
    if(grid[i][j].containsmine){
       state=LOSE;
        PlaySound(sound);
       endtime=GetTime();
	   Clear();
       }
	   else{
        if(grid[i][j].MinesAround==0){
            ClearAround(i,j);
        }blocksrevealed++;
        if(blocksrevealed==Cols*Rows-minespresent){
            state=WIN;
            endtime=GetTime();
        }
    }
    if(state==PLAYING &&  grid[i][j].revealed){
        PlaySound(sound2);
    }
}
void BlockTile(int i,int j){
    if(grid[i][j].revealed){
        return;
    }
    grid[i][j].tile=!grid[i][j].tile;
}
void BlockFlag(int i,int j){        
    if(grid[i][j].revealed){
        return;
    }
    grid[i][j].flagged=!grid[i][j].flagged;
    grid[i][j].tile=false;
}
int CountMines(int i,int j){
    int count=0;
    for(int m=-1;m<=1;m++){
        for(int n=-1;n<=1;n++){
            if(IsValidIndex(i+m,j+n)){
                if(grid[i+m][j+n].containsmine){
                    count++;
                }
            }
        }
    }
    return count;
}
void ClearAround(int i,int j){
    for(int m=-1;m<=1;m++){
        for(int n=-1;n<=1;n++){
            if(IsValidIndex(i+m,j+n)){
                if(!grid[i+m][j+n].revealed){
                    BlockReveal(i+m,j+n);
                }
            }
        }
    }
} 
void PlayAgain(){
    GridInIt();
    state=PLAYING;
    blocksrevealed=0;
    starttime=GetTime();
}
void GridInIt(){
       for(int i=0;i<Cols;i++){
                for(int j=0;j<Rows;j++){
                    grid[i][j]=(Block){
                        .i=i,
                        .j=j,
                        .revealed=false,
                        .containsmine=false,
                        .MinesAround=-1,
                        .flagged=false,
                        .tile=true
                   };
                }
            }
    minespresent=Rows*Cols /10;
    int MinesToPlace=minespresent;
    while(MinesToPlace>0){
        int i = rand() % Cols;
        int j = rand() % Rows;
        if(!grid[i][j].containsmine){
            grid[i][j].containsmine=true;
            MinesToPlace--;
        }
    }   
    for(int i=0;i<Cols;i++){
                for(int j=0;j<Rows;j++){
                    if(!grid[i][j].containsmine){
                        grid[i][j].MinesAround=CountMines(i,j);
                }
            }
    }
}
 

int main(){
	
    srand(time(0));

    InitWindow(screenwidth,screenheight,"MineSweeper");
    InitAudioDevice();

    flagSprite=LoadTexture("resources/flag.png");
	mineSprite=LoadTexture("resources/mine.png");
    emoji=LoadTexture("resources/sademoji.png");
    happyemoji=LoadTexture("resources/smile.png");
    sound=LoadSound("resources/sound.mp3");
    sound2=LoadSound("resources/sound2.wav");
    tileSprite=LoadTexture("resources/tile.png");

    PlayAgain();
    
    while(!WindowShouldClose()){
        if(IsMouseButtonPressed(MOUSE_BUTTON_LEFT)){
            Vector2 mpos = GetMousePosition();
            int indexI=mpos.x/blockwidth;
            int indexJ=mpos.y/blockheight;
            if(state==PLAYING && IsValidIndex(indexI,indexJ)){
                   BlockReveal(indexI,indexJ);
                   BlockTile(indexI,indexJ);
            }
        }else if(IsMouseButtonPressed(MOUSE_BUTTON_RIGHT)){
             Vector2 mpos = GetMousePosition();
            int indexI=mpos.x/blockwidth;
            int indexJ=mpos.y/blockheight;
            if(state==PLAYING && IsValidIndex(indexI,indexJ)){
                   BlockFlag(indexI,indexJ);
                   BlockTile(indexI,indexJ);
            }
        }
        if(IsKeyPressed(KEY_R)){
            PlayAgain();
        }
        
        BeginDrawing();
            ClearBackground(RAYWHITE);
            for(int i=0;i<Cols;i++){
                for(int j=0;j<Rows;j++){
                    DrawBlock (grid[i][j]);
                }
            }
           

        if(state==LOSE){
			
            DrawRectangle(0,0,screenwidth,screenheight,Fade(WHITE, 0.6f));
            DrawText(youlose,screenwidth/2 -MeasureText(youlose,20)/2,screenheight/2-10,20,BLACK);
            DrawText(restart,screenwidth/2-MeasureText(restart,20)/2,screenheight*0.75f-10,20,DARKGRAY);
            DrawTextureV(emoji,(Vector2) {screenwidth/4,screenheight/100},WHITE);
            int min=(int)(endtime-starttime)/60;
            int sec=(int)(endtime-starttime)%60;
            DrawText(TextFormat("Time played:%d minutes %d seconds",min,sec),20,screenheight-40,20,DARKGRAY);
          
            
        }    
         if(state==WIN){
            DrawRectangle(0,0,screenwidth,screenheight,Fade(WHITE, 0.6f));
            DrawText(youwin,screenwidth/2 -MeasureText(youwin,20)/2,screenheight/2-10,20,DARKGRAY);
            DrawText(restart,screenwidth/2-MeasureText(restart,20)/2,screenheight*0.75f-10,20,DARKGRAY);
            DrawTextureV(happyemoji,(Vector2) {screenwidth/3,screenheight/50},WHITE);
            int min=(int)(endtime-starttime)/60;
            int sec=(int)(endtime-starttime)%60;
            DrawText(TextFormat("Time played:%d minutes %d seconds",min,sec),20,350,20,DARKGRAY);
        }    
        EndDrawing();
    }
    CloseAudioDevice();
    CloseWindow();
    return 0;
}