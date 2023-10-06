#include <iostream>
#include <cstdlib>
#include <cpr/cpr.h>
#include <nlohmann/json.hpp>

using namespace std;
using json = nlohmann::json;

class Ingredient
{
	private:
		string nom;

	public:
		Ingredient(string nomm):nom{nomm}{}
		Ingredient(json data)
		{
			nom = data["nom"];
		}

		Ingredient(int id)
		{
			cpr::Response r = cpr::Get(cpr::Url{"http://localhost:8000/ingredient/"+to_string(id)});
			json m = json::parse(r.text);

			nom = m["nom"];
		}
		void Affichage()
		{
			cout << "Ingredient : " << nom << endl;
		}
		friend ostream& operator<<(ostream& out, const Ingredient& i) {
			return out << "Ingredient : " << i.nom;
		}

};

class Machine
{
	private:
		string nom;
		int prix;

	public:
		Machine(string nomm, int prixx):nom{nomm}, prix{prixx}{}
		Machine(json data)
		{
			nom = data["nom"];
			prix = data["prix"];
		}

		Machine(int id)
		{
			cpr::Response r = cpr::Get(cpr::Url{"http://localhost:8000/machine/"+to_string(id)});
			json m = json::parse(r.text);

			nom = m["nom"];
			prix = m["prix"];
		}
		void Affichage()
		{
			cout << "Machine : " << nom << "  prix : " << prix << endl;
		}

};

class Departement
{
	private:
		int numero;
		int prix_m2;

	public:
		Departement(int num, int prix_mcarre):numero{num}, prix_m2{prix_mcarre}{}
		Departement(json data)
		{
			numero = data["numero"];
			prix_m2 = data["prix_m2"];
		}

		Departement(int id)
		{
			cpr::Response r = cpr::Get(cpr::Url{"http://localhost:8000/departement/"+to_string(id)});
			json m = json::parse(r.text);

			numero = m["numero"];
			prix_m2 = m["prix_m2"];
		}
		void Affichage()
		{
			cout << "Département : " << numero << "  prix au m2 : " << prix_m2 << endl;
		}
		friend ostream& operator<<(ostream& out, const Departement& d) {
			return out << "Département : " << d.numero << "  prix au m2 : " << d.prix_m2 ;
		}
};

class Prix
{
	private:
		unique_ptr<Ingredient> ingredient;
		unique_ptr<Departement> departement;
		int prix;

	public:

		Prix(int id)
		{
			cpr::Response r = cpr::Get(cpr::Url{"http://localhost:8000/prix/"+to_string(id)});
			json m = json::parse(r.text);

			ingredient = make_unique<Ingredient>(m["ingredient"]);
			departement = make_unique<Departement>(m["departement"]);
			prix = m["prix"];
		}
		friend ostream& operator<<(ostream& out, const Prix& p) {
			return out << *p.ingredient << " " << *p.departement << "€ et coute " << p.prix << "€";
		}
};

class QuantiteIngredient
{
	private:
		unique_ptr<Ingredient> ingredient;
		int quantite;

	public:

		QuantiteIngredient(int id)
		{
			cpr::Response r = cpr::Get(cpr::Url{"http://localhost:8000/quantiteingredient/"+to_string(id)});
			json m = json::parse(r.text);

			ingredient = make_unique<Ingredient>(m["ingredient"]);
			quantite = m["quantite"];
		}
		friend ostream& operator<<(ostream& out, const QuantiteIngredient& q) {
			return out << "Il y a " << q.quantite << "kg de " << *q.ingredient ;
		}
};




auto main() -> int
{
	//Departement HauteGaronne{31, 1000};
	//HauteGaronne.Affichage();

	cpr::Response r = cpr::Get(cpr::Url{"http://localhost:8000/prix/1"});
	json m = json::parse(r.text);

	Prix lolo{1};
	QuantiteIngredient tdfe{1};
	cout << lolo << endl;
	cout << tdfe << endl;


	/*Departement HauteGaronne{m};
	HauteGaronne.Affichage();

	Departement HauteGaronne2{1};
	HauteGaronne2.Affichage();*/

	//cout << r.text << endl;
	//cout << m << endl;


}
