/**************************************************************************/
/*                                                                        */
/*                  Jens                                                  */
/*                                                                        */
/**************************************************************************/
/* Allows to display Jacobian Information of a mesh in .m3d format        */
/* Written by Claudio Lobos (clobos@inf.utfsm.cl) 2015					  */
/* UNIVERSIDAD TECNICA FEDERICO SANTA MARIA								  */
/**************************************************************************/

/*
 <JENS: this program computes the Element Normalized Scaled Jacobian (Jens)>

 Copyright (C) <2015>  <Claudio Lobos>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/gpl.txt>
 */

#include "Quality.h"

//--------------------------------------------------------------------------
//--------------------------------------------------------------------------
Quality::Quality()
{
}

//--------------------------------------------------------------------------
//--------------------------------------------------------------------------
Quality::~Quality()
{
}

//--------------------------------------------------------------------------
//--------------------------------------------------------------------------
void Quality::executeGeneralStatistics(vector<Point3D> &points, vector<Element *> &elements, Metric *metric)
{
    if (elements.empty())
    {
        cout << "no elements\n";
        return;
    }
    vector<int> histo(22, 0);
    double worst = 2, total = 0;

    vector<double> min_vals_type(4, 2), max_vals_type(4, -2), ave_vals_type(4, 0);
    vector<unsigned int> ele_quantity(4, 0);

    unsigned int type = 0;

    for (unsigned int i = 0; i < elements.size(); i++)
    {
        double qua = metric->getElementQuality(elements[i], points);
        total += qua;
        bool print = false;
        if (worst > qua)
            worst = qua;
        if (qua < 0)
        {
            histo[0]++;
            print = true;
        }
        else if (qua < 0.033333)
        {
            histo[1]++;
            print = true;
        }
        else if (qua < 0.05)
            histo[2]++;
        else if (qua < 0.1)
            histo[3]++;
        else if (qua < 0.15)
            histo[4]++;
        else if (qua < 0.2)
            histo[5]++;
        else if (qua < 0.25)
            histo[6]++;
        else if (qua < 0.3)
            histo[7]++;
        else if (qua < 0.35)
            histo[8]++;
        else if (qua < 0.4)
            histo[9]++;
        else if (qua < 0.45)
            histo[10]++;
        else if (qua < 0.5)
            histo[11]++;
        else if (qua < 0.55)
            histo[12]++;
        else if (qua < 0.6)
            histo[13]++;
        else if (qua < 0.65)
            histo[14]++;
        else if (qua < 0.7)
            histo[15]++;
        else if (qua < 0.75)
            histo[16]++;
        else if (qua < 0.8)
            histo[17]++;
        else if (qua < 0.85)
            histo[18]++;
        else if (qua < 0.9)
            histo[19]++;
        else if (qua < 0.95)
            histo[20]++;
        else
            histo[21]++;

        if (print)
        {
            cout << "Q: " << qua << " Index " << i << " " << *(elements[i]) << " 1000.0 0.45 1.0\n";
        }

        // find the type
        if (elements[i]->getCharType() == 'H')
        {
            type = 0;
        }
        else if (elements[i]->getCharType() == 'R')
        {
            type = 1;
        }
        else if (elements[i]->getCharType() == 'P')
        {
            type = 2;
        }
        else if (elements[i]->getCharType() == 'T')
        {
            type = 3;
        }

        // update min and max per element type.
        if (min_vals_type[type] > qua)
        {
            min_vals_type[type] = qua;
        }
        if (qua > max_vals_type[type])
        {
            max_vals_type[type] = qua;
        }

        ave_vals_type[type] += qua;
        ele_quantity[type]++;
    }
    cout << "negative: " << histo[0] << endl;
    cout << "<0.0333 : " << histo[1] << endl;
    float step = 0.05;
    for (int i = 2; i < 22; i++)
    {
        cout << "<" << step << "\t:" << histo[i] << endl;
        step += 0.05;
    }

    cout << "total: " << elements.size() << endl;
    cout << "worst quality " << worst << endl;
    cout << "average quality " << total / elements.size() << endl;

    cout << "\ntikz format\n";
    cout << "(-1," << histo[0] << ")\n";
    cout << "(0.03," << histo[1] << ")\n";
    step = 0.05;
    for (int i = 2; i < 22; i++)
    {
        cout << "(" << step << "," << histo[i] << ")\n";
        step += 0.05;
    }
    // cout << "(1," << histo[19] << ")\n";

    // print range of quality per element type
    cout << " > Quality per element type: Hex, Pri, Pyr, Tet respectively:\n";
    for (unsigned int i = 0; i < min_vals_type.size(); i++)
    {
        if (ele_quantity[i] == 0)
        {
            cout << "no elements of this type\n";
        }
        else
        {
            if (ele_quantity[i] >= 2)
            {
                cout << "[ " << min_vals_type[i] << "," << max_vals_type[i] << "] average: ";
                cout << ave_vals_type[i] / ele_quantity[i] << " (" << ele_quantity[i] << ")\n";
            }
            if (ele_quantity[i] == 1)
            {
                cout << "[ " << ave_vals_type[i] << "," << ave_vals_type[i] << "] average: ";
                cout << ave_vals_type[i] << " (" << ave_vals_type[i] << ")\n";
            }
        }
    }
}

//--------------------------------------------------------------------------
//--------------------------------------------------------------------------

//--------------------------------------------------------------------------
//--------------------------------------------------------------------------
void Quality::execute_JENS_Worst(vector<Point3D> &p, vector<Element *> &e)
{

    if (e.empty())
    {
        cout << "no elements\n";
        return;
    }

    double worst = 2;

    for (int i = 0; i < (int)e.size(); i++)
    {
        double qua = e[i]->getElementJENS(p);
        if (worst > qua)
            worst = qua;
    }

    cout << "  >worst quality " << worst << endl;
}

//--------------------------------------------------------------------------
//--------------------------------------------------------------------------
void Quality::execute_compareJensAndJeans(vector<Point3D> &p, vector<Element *> &e)
{

    if (e.empty())
    {
        cout << "no elements\n";
        return;
    }

    double worstE = 2, worstA = 2;

    for (int i = 0; i < (int)e.size(); i++)
    {
        double quaE = e[i]->getElementJENS(p);
        double quaA = e[i]->getElementJEANS(p);

        if (worstE > quaE)
            worstE = quaE;

        if (worstA > quaA)
            worstA = quaA;
    }

    cout << "(" << worstE << "," << worstA << ")\n";
}

//--------------------------------------------------------------------------
//--------------------------------------------------------------------------
void Quality::execute_allJENS(vector<Point3D> &p, vector<Element *> &e)
{

    cout << "Element index | and then Jens for each node of it:\n\n";

    for (unsigned int i = 0; i < e.size(); i++)
    {

        cout << i;
        vector<double> jens = e[i]->getJENS(p);
        vector<unsigned int> epts = e[i]->getPoints();

        for (unsigned int j = 0; j < jens.size(); j++)
        {
            cout << " (" << epts[j] << "," << jens[j] << ")";
        }

        cout << "\n";
    }
}

//--------------------------------------------------------------------------
//--------------------------------------------------------------------------
void Quality::execute_all(vector<Point3D> &p, vector<Element *> &e)
{

    for (unsigned int i = 0; i < e.size(); i++)
    {
        vector<double> js = e[i]->getJS(p);
        vector<double> jens = e[i]->getJENS(p);

        double worst_js = 2, worst_jens = 2;

        for (unsigned int j = 0; j < jens.size(); j++)
        {
            // cout << " " << jens[j] << "(" << js[j] << ")";
            bool update_jens = false, update_js = false;
            if (worst_jens > jens[j])
            {
                worst_jens = jens[j];
                update_jens = true;
            }
            if (worst_js > js[j])
            {
                worst_js = js[j];
                update_js = true;
            }
            /*if (update_jens!=update_js) {
                cout <<
                cout << "\njs and jens contradiction at Quality::execute_all\n";
            }*/
        }
        // cout << " -> " << worst_jens << "(" << worst_js << ")\n";
        cout << worst_jens << "\n";
    }
}

//--------------------------------------------------------------------------
//--------------------------------------------------------------------------
void Quality::execute_allAR(vector<Point3D> &p, vector<Element *> &e)
{

    for (unsigned int i = 0; i < e.size(); i++)
    {
        cout << "ARf " << e[i]->getAspectRatio(p) << " ARe ";
        cout << e[i]->getEdgeAspectRatio(p) << "\n";
    }
}

//--------------------------------------------------------------------------
//--------------------------------------------------------------------------
/*void Quality::execute_ScaledJacVsARG(vector<Point3D> &points, vector<Element *> &elements) {

    double max_pos_dif = 0, max_neg_dif =0, avg_dif = 0;
    double qarg = 0, qjens = 0;
    unsigned int worst_pos_idx = 0, worst_neg_idx = 0;

    unsigned int tetcount = 0, posdif = 0, negdif = 0;

    for (unsigned int i=0; i<elements.size(); i++) {
        if (elements[i]->getCharType()!='T') {
            continue;
        }

        tetcount++;

        //compute the Scaled Jac
        qjens = elements[i]->getWorstScaledJac(points);

        //compute the Aspect Ratio Gamma
        vector<int> tpoints = elements[i]->getElement()->getPoints();

        Point p0 = points[tpoints[0]].getPoint();
        Point p1 = points[tpoints[1]].getPoint();
        Point p2 = points[tpoints[2]].getPoint();
        Point p3 = points[tpoints[3]].getPoint();

        double edgelents = 0;

        Point dif1 = p1 - p0;
        edgelents += dif1.dot(dif1);

        Point dif2 = p2 - p0;
        edgelents += dif2.dot(dif2);

        Point dif3 = p3 - p0;
        edgelents += dif3.dot(dif3);

        Point dif = p1 - p2;
        edgelents += dif.dot(dif);

        dif = p1 - p3;
        edgelents += dif.dot(dif);

        dif = p2 - p3;
        edgelents += dif.dot(dif);

        edgelents /= 6;

        double volume = dif3.dot(dif1.cross(dif2)) / 6;

        qarg = (12*volume)/(pow(edgelents,1.5)*sqrt(2));

        double current_dif = qarg - qjens;
        if (current_dif>0) {
            posdif++;
            if (current_dif > max_pos_dif) {
                max_pos_dif = current_dif;
                worst_pos_idx = i;
            }
            avg_dif += current_dif;
        }
        else {
            negdif++;
            if (current_dif < max_neg_dif) {
                max_neg_dif = current_dif;
                worst_neg_idx = i;
            }
            avg_dif -= current_dif;

           // cout << "args " << qarg << " jens " << qjens << "\n";
        }

    }

    if (tetcount == 0) {
        cout << "no tets\n";
        return;
    }
    cout << "total tested " << tetcount << "\n";
    cout << "max pos dif: " << max_pos_dif << " (of " << posdif << ")\n";
    cout << "max neg dif: " << max_neg_dif << " (of " << negdif << ")\n";
    cout << "average dif: " << avg_dif/tetcount << "\n";

    cout << "worst positive difference " << worst_pos_idx << ":\n";

    vector<int> tpoints = elements[worst_pos_idx]->getElement()->getPoints();
    for (unsigned int i=0; i<tpoints.size(); i++) {
        cout << " " << tpoints[i];
    }
    cout << " 1 1 1\n";

    cout << "worst negative difference " << worst_neg_idx << ":\n";

    tpoints = elements[worst_neg_idx]->getElement()->getPoints();
    for (unsigned int i=0; i<tpoints.size(); i++) {
        cout << " " << tpoints[i];
    }
    cout << " 1 1 1\n";
}*/

//--------------------------------------------------------------------------
//--------------------------------------------------------------------------
/*void Quality::execute_JS(vector<Point3D> &p, vector<Element *> &e){

    if (e.empty()){
        cout << "no elements\n";
        return;
    }
    vector<int> histo (22,0);
    double worst = 2, total = 0;

    vector<double> min_vals_type (4,2), max_vals_type (4,-2), ave_vals_type (4,0);
    vector<unsigned int> ele_quantity (4,0);

    unsigned int type = 0;

    for (int i=0; i<(int)e.size(); i++) {
        double qua = e[i]->getElementJS(p);
        total += qua;
        bool print = false;
        if(worst > qua)
            worst = qua;
        if(qua<0){
            histo[0]++;
            print = true;
        }
        else if(qua<0.033333){
            histo[1]++;
            print = true;
        }
        else if(qua<0.05)
            histo[2]++;
        else if(qua<0.1)
            histo[3]++;
        else if(qua<0.15)
            histo[4]++;
        else if(qua<0.2)
            histo[5]++;
        else if(qua<0.25)
            histo[6]++;
        else if(qua<0.3)
            histo[7]++;
        else if(qua<0.35)
            histo[8]++;
        else if(qua<0.4)
            histo[9]++;
        else if(qua<0.45)
            histo[10]++;
        else if(qua<0.5)
            histo[11]++;
        else if(qua<0.55)
            histo[12]++;
        else if(qua<0.6)
            histo[13]++;
        else if(qua<0.65)
            histo[14]++;
        else if(qua<0.7)
            histo[15]++;
        else if(qua<0.75)
            histo[16]++;
        else if(qua<0.8)
            histo[17]++;
        else if(qua<0.85)
            histo[18]++;
        else if(qua<0.9)
            histo[19]++;
        else if(qua<0.95)
            histo[20]++;
        else
            histo[21]++;

        if (print) {
            cout << "Q: " << qua << " Index " << i << " " << *(e[i]) << " 1000.0 0.45 1.0\n";
        }

        //find the type
        if(e[i]->getCharType()=='H') {
            type=0;
        }
        else if(e[i]->getCharType()=='R') {
            type=1;
        }
        else if(e[i]->getCharType()=='P') {
            type=2;
        }
        else if(e[i]->getCharType()=='T') {
            type=3;
        }

        //update min and max per element type.
        if(min_vals_type[type] > qua){
            min_vals_type[type] = qua;
        }
        if(qua > max_vals_type[type]){
            max_vals_type[type] = qua;
        }

        ave_vals_type[type] += qua;
        ele_quantity[type]++;

    }
    cout << "negative: " << histo[0] << endl;
    cout << "<0.0333 : " << histo[1] << endl;
    float step = 0.05;
    for(int i=2;i<22;i++) {
        cout << "<" << step << "\t:" << histo[i] << endl;
        step+=0.05;
    }

    cout << "total: " << e.size() << endl;
    cout << "worst quality " << worst << endl;
    cout << "average quality " << total/e.size() << endl;

    cout << "\ntikz format\n";
    cout << "(-1," << histo[0] << ")\n";
    cout << "(0.03," << histo[1] << ")\n";
    step = 0.05;
    for(int i=2;i<22;i++){
        cout << "(" << step << "," << histo[i] << ")\n";
        step+=0.05;
    }
    //cout << "(1," << histo[19] << ")\n";

    //print range of quality per element type
    cout << " > Quality per element type: Hex, Pri, Pyr, Tet respectively:\n";
    for (unsigned int i=0; i<min_vals_type.size(); i++) {
        if (ele_quantity[i]>=2) {
            cout << "[ " << min_vals_type[i] << "," << max_vals_type[i] << "] average: ";
            cout << ave_vals_type[i]/ele_quantity[i] << " (" << ele_quantity[i] << ")\n";
        }
        if (ele_quantity[i]==1) {
            cout << "[ " << ave_vals_type[i] << "," << ave_vals_type[i] << "] average: ";
            cout << ave_vals_type[i] << " (" << ave_vals_type[i] << ")\n";
        }
        else {
            cout << "no elements of this type\n";
        }
    }
}

//--------------------------------------------------------------------------
//--------------------------------------------------------------------------
void Quality::execute_JENS(vector<Point3D> &p, vector<Element *> &e){

    if (e.empty()){
        cout << "no elements\n";
        return;
    }
    vector<int> histo (22,0);
    double worst = 2, total = 0;

    vector<double> min_vals_type (4,2), max_vals_type (4,-2), ave_vals_type (4,0);
    vector<unsigned int> ele_quantity (4,0);

    unsigned int type = 0;

    for (int i=0; i<(int)e.size(); i++) {
        double qua = e[i]->getElementJENS(p);
        total += qua;
        bool print = false;
        if(worst > qua)
            worst = qua;
        if(qua<0){
            histo[0]++;
            print = true;
        }
        else if(qua<0.033333){
            histo[1]++;
            print = true;
        }
        else if(qua<0.05)
            histo[2]++;
        else if(qua<0.1)
            histo[3]++;
        else if(qua<0.15)
            histo[4]++;
        else if(qua<0.2)
            histo[5]++;
        else if(qua<0.25)
            histo[6]++;
        else if(qua<0.3)
            histo[7]++;
        else if(qua<0.35)
            histo[8]++;
        else if(qua<0.4)
            histo[9]++;
        else if(qua<0.45)
            histo[10]++;
        else if(qua<0.5)
            histo[11]++;
        else if(qua<0.55)
            histo[12]++;
        else if(qua<0.6)
            histo[13]++;
        else if(qua<0.65)
            histo[14]++;
        else if(qua<0.7)
            histo[15]++;
        else if(qua<0.75)
            histo[16]++;
        else if(qua<0.8)
            histo[17]++;
        else if(qua<0.85)
            histo[18]++;
        else if(qua<0.9)
            histo[19]++;
        else if(qua<0.95)
            histo[20]++;
        else
            histo[21]++;

        if (print) {
            cout << "Q: " << qua << " Index " << i << " " << *(e[i]) << " 1000.0 0.45 1.0\n";
        }

        //find the type
        if(e[i]->getCharType()=='H') {
            type=0;
        }
        else if(e[i]->getCharType()=='R') {
            type=1;
        }
        else if(e[i]->getCharType()=='P') {
            type=2;
        }
        else if(e[i]->getCharType()=='T') {
            type=3;
        }

        //update min and max per element type.
        if(min_vals_type[type] > qua){
            min_vals_type[type] = qua;
        }
        if(qua > max_vals_type[type]){
            max_vals_type[type] = qua;
        }

        ave_vals_type[type] += qua;
        ele_quantity[type]++;

    }

    cout << "negative: " << histo[0] << endl;
    cout << "<0.0333 : " << histo[1] << endl;
    float step = 0.05;
    for(int i=2;i<22;i++) {
        cout << "<" << step << "\t:" << histo[i] << endl;
        step+=0.05;
    }

    cout << "total: " << e.size() << endl;
    cout << "worst quality " << worst << endl;
    cout << "average quality " << total/e.size() << endl;

    cout << "\ntikz format\n";
    cout << "(-1," << histo[0] << ")\n";
    cout << "(0.03," << histo[1] << ")\n";
    step = 0.05;
    for(int i=2;i<22;i++){
        cout << "(" << step << "," << histo[i] << ")\n";
        step+=0.05;
    }
    //cout << "(1," << histo[19] << ")\n";

    //print range of quality per element type
    cout << " > Quality per element type: Hex, Pri, Pyr, Tet respectively:\n";
    for (unsigned int i=0; i<min_vals_type.size(); i++) {
        if (ele_quantity[i]>=2) {
            cout << "[ " << min_vals_type[i] << "," << max_vals_type[i] << "] average: ";
            cout << ave_vals_type[i]/ele_quantity[i] << " (" << ele_quantity[i] << ")\n";
        }
        if (ele_quantity[i]==1) {
            cout << "[ " << ave_vals_type[i] << "," << ave_vals_type[i] << "] average: ";
            cout << ave_vals_type[i] << " (" << ave_vals_type[i] << ")\n";
        }
        else {
            cout << "no elements of this type\n";
        }
    }
}


//--------------------------------------------------------------------------
//--------------------------------------------------------------------------
void Quality::execute_JEANS(vector<Point3D> &p, vector<Element *> &e){

    if (e.empty()){
        cout << "no elements\n";
        return;
    }
    vector<int> histo (22,0);
    double worst = 2, total = 0;

    vector<double> min_vals_type (4,2), max_vals_type (4,-2), ave_vals_type (4,0);
    vector<unsigned int> ele_quantity (4,0);

    unsigned int type = 0;

    for (int i=0; i<(int)e.size(); i++) {
        double qua = e[i]->getElementJEANS(p);
        total += qua;
        bool print = false;
        if(worst > qua)
            worst = qua;
        if(qua<0){
            histo[0]++;
            print = true;
        }
        else if(qua<0.033333){
            histo[1]++;
            print = true;
        }
        else if(qua<0.05)
            histo[2]++;
        else if(qua<0.1)
            histo[3]++;
        else if(qua<0.15)
            histo[4]++;
        else if(qua<0.2)
            histo[5]++;
        else if(qua<0.25)
            histo[6]++;
        else if(qua<0.3)
            histo[7]++;
        else if(qua<0.35)
            histo[8]++;
        else if(qua<0.4)
            histo[9]++;
        else if(qua<0.45)
            histo[10]++;
        else if(qua<0.5)
            histo[11]++;
        else if(qua<0.55)
            histo[12]++;
        else if(qua<0.6)
            histo[13]++;
        else if(qua<0.65)
            histo[14]++;
        else if(qua<0.7)
            histo[15]++;
        else if(qua<0.75)
            histo[16]++;
        else if(qua<0.8)
            histo[17]++;
        else if(qua<0.85)
            histo[18]++;
        else if(qua<0.9)
            histo[19]++;
        else if(qua<0.95)
            histo[20]++;
        else
            histo[21]++;

        if (print) {
            cout << "Q: " << qua << " Index " << i << " " << *(e[i]) << " 1000.0 0.45 1.0\n";
        }

        //find the type
        if(e[i]->getCharType()=='H') {
            type=0;
        }
        else if(e[i]->getCharType()=='R') {
            type=1;
        }
        else if(e[i]->getCharType()=='P') {
            type=2;
        }
        else if(e[i]->getCharType()=='T') {
            type=3;
        }

        //update min and max per element type.
        if(min_vals_type[type] > qua){
            min_vals_type[type] = qua;
        }
        if(qua > max_vals_type[type]){
            max_vals_type[type] = qua;
        }

        ave_vals_type[type] += qua;
        ele_quantity[type]++;

    }

    cout << "negative: " << histo[0] << endl;
    cout << "<0.0333 : " << histo[1] << endl;
    float step = 0.05;
    for(int i=2;i<22;i++) {
        cout << "<" << step << "\t:" << histo[i] << endl;
        step+=0.05;
    }

    cout << "total: " << e.size() << endl;
    cout << "worst quality " << worst << endl;
    cout << "average quality " << total/e.size() << endl;

    cout << "\ntikz format\n";
    cout << "(-1," << histo[0] << ")\n";
    cout << "(0.03," << histo[1] << ")\n";
    step = 0.05;
    for(int i=2;i<22;i++){
        cout << "(" << step << "," << histo[i] << ")\n";
        step+=0.05;
    }
    //cout << "(1," << histo[19] << ")\n";

    //print range of quality per element type
    cout << " > Quality per element type: Hex, Pri, Pyr, Tet respectively:\n";
    for (unsigned int i=0; i<min_vals_type.size(); i++) {
        if (ele_quantity[i]>=2) {
            cout << "[ " << min_vals_type[i] << "," << max_vals_type[i] << "] average: ";
            cout << ave_vals_type[i]/ele_quantity[i] << " (" << ele_quantity[i] << ")\n";
        }
        if (ele_quantity[i]==1) {
            cout << "[ " << ave_vals_type[i] << "," << ave_vals_type[i] << "] average: ";
            cout << ave_vals_type[i] << " (" << ave_vals_type[i] << ")\n";
        }
        else {
            cout << "no elements of this type\n";
        }
    }
}*/
