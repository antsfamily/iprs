
figure
A = imread('./small.tiff');
imshow(A)


EPS  = 1.0e-16;
sf = [0, 200];
st = [0, 255];
filename = 'E2_84686_STD_L0_F203';
% filename = 'E2_84686_STD_L0_F203_SI';
% filename = 'E2_84690_STD_L0_F137_SI';
filename = 'E2_84690_STD_L0_F137_2_SI';
filename = 'Vancouver(sa0ea19438sr0er9288)_CSA_Imaging';
% filename = 'Vancouver(sa7657ea9193sr1850er3898)_CSA_Imaging';

load(['./', filename, '.mat']);


SI = abs(SI);

% load('./SI.mat');

SI = 20 *log10(SI + EPS);

SI = scale(SI, sf, st);

figure,imagesc(SI);axis image;set(gcf,'Color','w');
% axis([-61789.06113078  65134.7516856  -64387.99065362  64387.99065362])
axis square