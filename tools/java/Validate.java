import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.*;
import com.clarkparsia.pellet.owlapiv3.PelletReasonerFactory;
import java.io.File;
import java.util.*;

public class Validate {
  public static void main(String[] a) throws Exception {
    OWLOntologyManager m = OWLManager.createOWLOntologyManager();
    OWLOntology o = m.loadOntologyFromOntologyDocument(new File(a[0]));
    Map<String,Integer> byType = new TreeMap<>();
    int rules=0, logical=0, decl=0, annot=0, abox=0, tbox=0, rbox=0, swrlAtoms=0;
    for (OWLAxiom ax : o.getAxioms()) {
      String t = ax.getAxiomType().getName();
      byType.merge(t,1,Integer::sum);
      if (ax instanceof SWRLRule) { rules++; SWRLRule r=(SWRLRule)ax; swrlAtoms += r.getBody().size()+r.getHead().size(); continue; }
      if (ax.isOfType(AxiomType.DECLARATION)) decl++;
      else if (ax.isAnnotationAxiom()) annot++;
      else if (ax.isOfType(AxiomType.ABoxAxiomTypes)) abox++;
      else if (ax.isOfType(AxiomType.TBoxAxiomTypes)) tbox++;
      else if (ax.isOfType(AxiomType.RBoxAxiomTypes)) rbox++;
    }
    int total = o.getAxiomCount();
    System.out.println("FILE=" + a[0]);
    System.out.println("TOTAL_AXIOMS=" + total);
    System.out.println("LOGICAL_AXIOMS=" + o.getLogicalAxiomCount());
    System.out.println("CLASSES=" + o.getClassesInSignature().size());
    System.out.println("OBJECT_PROPERTIES=" + o.getObjectPropertiesInSignature().size());
    System.out.println("DATA_PROPERTIES=" + o.getDataPropertiesInSignature().size());
    System.out.println("INDIVIDUALS=" + o.getIndividualsInSignature().size());
    System.out.println("SWRL_RULES=" + rules + " SWRL_ATOMS=" + swrlAtoms);
    System.out.println("DECLARATION=" + decl + " ANNOTATION=" + annot + " TBOX=" + tbox + " RBOX=" + rbox + " ABOX=" + abox);
    for (Map.Entry<String,Integer> e : byType.entrySet()) System.out.println("  " + e.getKey() + "=" + e.getValue());
    if (a.length > 1) {
      OWLReasoner r = PelletReasonerFactory.getInstance().createReasoner(o);
      System.out.println("CONSISTENT=" + r.isConsistent());
      OWLDataFactory df = m.getOWLDataFactory();
      String ns = "http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#";
      for (String c : a[1].split(",")) {
        Set<OWLNamedIndividual> s = r.getInstances(df.getOWLClass(IRI.create(ns + c)), false).getFlattened();
        List<String> n = new ArrayList<>(); for (OWLNamedIndividual i : s) n.add(i.getIRI().getFragment());
        Collections.sort(n);
        System.out.println("INSTANCES " + c + " (" + n.size() + ") = " + n);
      }
      OWLNamedIndividual bb = df.getOWLNamedIndividual(IRI.create(ns + "Sektor_BarangBaku"));
      System.out.println("Sektor_BarangBaku skorOutlookAktif = " + r.getDataPropertyValues(bb, df.getOWLDataProperty(IRI.create(ns + "skorOutlookAktif"))));
      OWLNamedIndividual antm = df.getOWLNamedIndividual(IRI.create(ns + "ANTM"));
      System.out.println("ANTM skorTotalEmiten = " + r.getDataPropertyValues(antm, df.getOWLDataProperty(IRI.create(ns + "skorTotalEmiten"))));
    }
  }
}
