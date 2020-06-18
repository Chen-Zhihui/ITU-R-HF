// Operating system preprocessor directives *********************************************************
#ifdef _WIN32
	#define DLLEXPORT __declspec(dllexport)
#endif
#ifdef __linux__
	#define DLLEXPORT
#endif
#ifdef __APPLE__
	#define DLLEXPORT
#endif
// End operating system preprocessor directives *****************************************************

/********************************* Defines ************************************/

// Version number
#define P372VER		"14.1"

// Have the preprocessor time stamp the compile time
#define P372CT		__TIMESTAMP__

// Noise calculation (See ITU-R P.372)
#define CITY		0.0
#define RESIDENTIAL 1.0
#define RURAL		2.0
#define QUIETRURAL	3.0
#define NOISY		4.0
#define	QUIET		5.0


// Return ERROR >= 200 and < 220

// Return ERROR from ReadFamDud()
#define RTN_ERROPENCOEFFFILE			201 // ERROR: Can Not Open Coefficient File

// Return ERROR from AllocatePathMemory(), FreePathMemory() and InputDump()
#define RTN_ERRALLOCATEDUD				202 // ERROR: Allocating Memory for DuD
#define RTN_ERRALLOCATEFAM				203 // ERROR: Allocating Memory for Fam
#define RTN_ERRALLOCATEFAKP				204 // ERROR: Allocating Memory for FakP
#define RTN_ERRALLOCATEFAKABP			205 // ERROR: Allocating Memory for FakABP// Return ERROR from P533()
#define RTN_ERRP372DLL					206 // ERROR: Can Not Open P372.DLL
#define RTN_ERRALLOCATENOISE            207 // ERROR: Allocating Memory for Noise Structure

// Return OKAY > 20 and <= 30
#define RTN_ALLOCATEP372OK				21 // AllocatePathMemory()
#define RTN_READFAMDUDOK				22 // ReadFamDud()
#define RTN_NOISEFREED					23 // NoiseMemory.c FreeNoiseMemory()
#define RTN_NOISEOK						24 // Noise()
#define RTN_NOISEMANMADEOK				25 // Noise() Man-made noise override


/******************************* End Defines **********************************/

// Struct Definitions

struct FamStats {
	int tmblk;			// Timeblock
	double FA;			// Atmospheric noise in dB above kT0b at 1 MHz
	double SigmaFam;	// Standard deviation of values, Fam
	double Du;			// Ratio of upper decile to median value, Fam
	double SigmaDu;		// Standard deviations of values of Du
	double Dl;			// Ratio of median value, Fam, to lower decile
	double SigmaDl;		// Standard deviation of values of Dl
};

struct NoiseParams {
  // Output Parameters
  double FaA;  // Atmospheric noise
  double DuA;  // Atmospheric noise upper decile
  double DlA;  // Atmospheric noise lower decile
  double FaM;  // Man-made noise
  double DuM;  // Man-made noise upper decile
  double DlM;  // Man-made noise lower decile
  double FaG;  // Galactic noise
  double DuG;  // Galactic noise upper decile
  double DlG;  // Galactic noise lower decile
  double DuT;  // Total noise upper decile
  double DlT;  // Total noise lower decile
  double FamT; // Total noise

  // Non-Output Parameters
  double ManMadeNoise;
  double ***fakp;
  double **fakabp;
  double **fam;
  double ***dud;

};

// End Structures

// Prototypes
DLLEXPORT int AllocateNoiseMemory(struct NoiseParams *noiseP);
DLLEXPORT int FreeNoiseMemory(struct NoiseParams *noiseP);
DLLEXPORT int Noise(struct NoiseParams *noiseP, int hour, double lng, double lat, double frequency);
DLLEXPORT int ReadFamDud(struct NoiseParams *noiseP, const char *DataFilePath, int month);
DLLEXPORT void InitializeNoise(struct NoiseParams *noiseP);
DLLEXPORT char const * P372CompileTime();
DLLEXPORT char const * P372Version();
//DLLEXPORT 
// End Prototypes
