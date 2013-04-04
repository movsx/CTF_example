// Разбор "RGB analog component video" в виде "осциллографа" (C++/Qt)
// Ссылка на входные данные для задачи: http://dl.dropbox.com/u/17463542/forensics/task-data.zip
#include <QImage>
#include <cassert>
#include <algorithm>
#include <QColor>
#include <QString>
#include <QDebug>
typedef long long int64;
QImage img[106];
QImage result;
bool loaded[106];
const int shift = 419;
const int len = 1344;
const int hope_screen_width = 1344;
const int hope_pixel_width = 1;
const double color_mult = 2.55;

void checkImg(int id) {
	if(loaded[id]) return ;
	for(int i = 0; i < 106; i++) if(loaded[i] && abs(i - id) > 2) { img[i] = QImage(); loaded[i] = false; }
	qDebug() << id;
	QString filename = QString("%1.png").arg(id, 8);
	for(int j = 0; j < 8; j++) if(filename[j] == ' ') filename[j] = '0';
	img[id] = QImage(filename);
	loaded[id] = true;
}


int getPixelValue(int x, int color) {
	checkImg(x / 10000);
	int start = 321 + 110 * color;
	QRgb req;
	switch(color) {
		case 0: req = QColor(0x00, 0xff, 0xff).rgb(); break;
		case 1: req = QColor(0xff, 0xff, 0x00).rgb(); break;
		case 2: req = QColor(0xff, 0x00, 0xff).rgb(); break;
	}
	bool ok = false;
	int ok_start = 0, ok_end = 0;
	int ok_sum = 0;
	int ok_cnt = 0;
	for(int i = 0; i < 100; i++) {
		QRgb c = img[x / 10000].pixel(x % 10000, start - i);
		if(c == req) {
			ok_sum += i;
			ok_cnt++;
			ok_start = i;
			ok = true;
		} else {
			ok_end = i;
			if(ok) {
				//return ok_start;
				//return (ok_start + ok_end) / 2;
			}
		}
	}
	return ok_cnt ? (ok_sum/ok_cnt) : 0;
}

void solve() {
	int skip = 0;
	int pos = 419 + skip * len;

	int row = 0;
	while(pos + len < 106 * 10000) {
		qDebug() << "pos" << pos;
		for(int i = 0; i < hope_screen_width; i++) {
			int val[3] = {0};

			int cur_pix = (len / double(hope_screen_width) * i + .5);
			double w = len / double(hope_screen_width) * i - cur_pix;
			for(int j = 0; j < hope_pixel_width; j++)
				for(int k = 0; k < 3; k++) {
					val[k] = getPixelValue(pos + cur_pix + j + 1, k) * color_mult;
						/*
					val[k] = getPixelValue(pos + cur_pix + j, k) * color_mult * w
						   + getPixelValue(pos + cur_pix + j + 1, k) * color_mult * (1.0 - w);
						   */
				}
			assert(0 <= val[0] && val[0] <= 255);
			assert(0 <= val[1] && val[1] <= 255);
			assert(0 <= val[2] && val[2] <= 255);
			int colval = (val[0] << 16) | (val[1] << 8) | val[2];
			//qDebug() << row << i << colval;
			result.setPixel(i, row, colval);
		}
		pos += len;
		row++;
	}
}

int main() {
	result = QImage(hope_screen_width, 800, QImage::Format_RGB32);
	solve();
	result.save("result.png");
	return 0;
}
